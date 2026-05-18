from __future__ import annotations

import json
from pathlib import Path

from app.core.exceptions import ModelInferenceException
from app.llm.client import LLMClient
from app.rag.base_retriever import BaseRetriever
from app.rag.vector_retriever import VectorRetriever
from app.schemas.question import QuestionPipelineRequest, QuestionPipelineResponse, SourceDocument

_PROMPTS_DIR = Path(__file__).resolve().parents[1] / "llm" / "prompts"


def _build_context(sources: list[SourceDocument]) -> str:
    if not sources:
        return ""
    parts = []
    for i, doc in enumerate(sources, start=1):
        parts.append(f"[{i}] {doc.title}\n{doc.chunk}")
    return "\n\n".join(parts)


class QuestionService:
    def __init__(
        self,
        llm_client: LLMClient | None = None,
        retriever: BaseRetriever | None = None,
        prompt_file: str | None = None,
        rewrite_prompt_file: str | None = None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()
        self.retriever = retriever or VectorRetriever()
        self.prompt_file = prompt_file or str(_PROMPTS_DIR / "question_system.txt")
        self._rewrite_prompt = Path(
            rewrite_prompt_file or str(_PROMPTS_DIR / "query_rewrite_system.txt")
        ).read_text(encoding="utf-8")

    async def _rewrite_query(self, question: str) -> str:
        raw = await self.llm_client.chat_with_history(
            system_prompt=self._rewrite_prompt,
            history=[],
            user_prompt=question,
        )
        output = self.llm_client.extract_json(raw)
        return output.get("query", question)

    async def execute(self, request: QuestionPipelineRequest) -> QuestionPipelineResponse:
        search_query = await self._rewrite_query(request.original_user_input)
        sources = await self.retriever.retrieve(search_query)

        user_prompt = json.dumps(
            {
                "request_id": request.request_id,
                "question": request.original_user_input,
                "context": _build_context(sources),
            },
            ensure_ascii=False,
        )

        history = [{"role": msg.role, "content": msg.content} for msg in request.history]

        raw_text = await self.llm_client.chat_with_history_from_file(
            prompt_file=self.prompt_file,
            history=history,
            user_prompt=user_prompt,
        )

        llm_output = self.llm_client.extract_json(raw_text)

        try:
            answer = llm_output["answer"]
        except KeyError as e:
            raise ModelInferenceException(
                message="LLM 질의응답 응답에 필수 필드가 없습니다.",
                details={"missing_key": str(e)},
            ) from e

        if not isinstance(answer, str) or not answer.strip():
            raise ModelInferenceException(
                message="LLM 질의응답 응답의 answer가 유효하지 않습니다.",
                details={"answer": answer},
            )

        return QuestionPipelineResponse(
            request_id=request.request_id,
            answer=answer,
            sources=sources,
        )
