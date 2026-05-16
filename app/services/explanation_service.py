from __future__ import annotations

import json
from pathlib import Path

from app.core.exceptions import ModelInferenceException
from app.llm.client import LLMClient
from app.rag.base_retriever import BaseRetriever
from app.rag.vector_retriever import VectorRetriever
from app.schemas.explanation import (
    ComparisonExplanationRequest,
    ExplanationRequest,
    ExplanationResponse,
    PredictionExplanationRequest,
)
from app.schemas.question import SourceDocument

_PROMPTS_DIR = Path(__file__).resolve().parents[1] / "llm" / "prompts"


def _build_context(sources: list[SourceDocument]) -> str:
    if not sources:
        return ""
    parts = [f"[{i}] {doc.title}\n{doc.chunk}" for i, doc in enumerate(sources, start=1)]
    return "\n\n".join(parts)


def _round_floats(obj: object) -> object:
    if isinstance(obj, float):
        if abs(obj) >= 1e5 or (0 < abs(obj) < 0.01):
            return float(f"{obj:.2e}")
        return round(obj, 2)
    if isinstance(obj, dict):
        return {k: _round_floats(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_round_floats(v) for v in obj]
    return obj


class ExplanationService:
    def __init__(
        self,
        llm_client: LLMClient | None = None,
        retriever: BaseRetriever | None = None,
        prediction_prompt_file: str | None = None,
        optimization_prompt_file: str | None = None,
        comparison_prompt_file: str | None = None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()
        self.retriever = retriever or VectorRetriever()
        self.prediction_prompt_file = prediction_prompt_file or str(
            _PROMPTS_DIR / "explain_prediction_system.txt"
        )
        self.optimization_prompt_file = optimization_prompt_file or str(
            _PROMPTS_DIR / "explain_optimization_system.txt"
        )
        self.comparison_prompt_file = comparison_prompt_file or str(
            _PROMPTS_DIR / "explain_comparison_system.txt"
        )

    async def execute(self, request: ExplanationRequest) -> ExplanationResponse:
        if isinstance(request, PredictionExplanationRequest):
            prompt_file = self.prediction_prompt_file
        elif isinstance(request, ComparisonExplanationRequest):
            prompt_file = self.comparison_prompt_file
        else:
            prompt_file = self.optimization_prompt_file

        sources = await self.retriever.retrieve(request.original_user_input)
        context = _build_context(sources)

        payload = request.model_dump(exclude_none=True, exclude={"history", "task_type"})
        payload["context"] = context

        user_prompt = json.dumps(_round_floats(payload), ensure_ascii=False)

        history = [{"role": msg.role, "content": msg.content} for msg in request.history]

        # LLMClient 내부에서 ModelNotReadyException / ModelInferenceException 발생 가능
        llm_raw_text = await self.llm_client.chat_with_history_from_file(
            prompt_file=prompt_file,
            history=history,
            user_prompt=user_prompt,
        )

        # LLMClient 내부에서 ModelInferenceException 발생 가능
        llm_output = self.llm_client.extract_json(llm_raw_text)

        try:
            request_id = llm_output["request_id"]
            summary = llm_output["summary"]
            details = llm_output["details"]
        except KeyError as e:
            raise ModelInferenceException(
                message="LLM 설명 응답에 필수 필드가 없습니다.",
                details={"missing_key": str(e)},
            ) from e

        if request_id != request.request_id:
            raise ModelInferenceException(
                message="LLM 설명 응답의 request_id가 요청과 일치하지 않습니다.",
                details={"expected": request.request_id, "received": request_id},
            )

        if not isinstance(summary, str) or not summary.strip():
            raise ModelInferenceException(
                message="LLM 설명 응답의 summary가 유효하지 않습니다.",
                details={"summary": summary},
            )

        if (
            not isinstance(details, list)
            or not details
            or not all(isinstance(d, str) for d in details)
        ):
            raise ModelInferenceException(
                message="LLM 설명 응답의 details가 유효하지 않습니다.",
                details={"details": details},
            )

        return ExplanationResponse(
            request_id=request_id,
            summary=summary,
            details=details,
        )