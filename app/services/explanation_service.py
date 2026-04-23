from __future__ import annotations

import json
from pathlib import Path

from app.core.exceptions import ModelInferenceException
from app.llm.client import LLMClient
from app.schemas.explanation import (
    ExplanationRequest,
    ExplanationResponse,
    PredictionExplanationRequest,
)

_PROMPTS_DIR = Path(__file__).resolve().parents[1] / "llm" / "prompts"


class ExplanationService:
    def __init__(
        self,
        llm_client: LLMClient | None = None,
        prediction_prompt_file: str | None = None,
        optimization_prompt_file: str | None = None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()
        self.prediction_prompt_file = prediction_prompt_file or str(
            _PROMPTS_DIR / "explain_prediction_system.txt"
        )
        self.optimization_prompt_file = optimization_prompt_file or str(
            _PROMPTS_DIR / "explain_optimization_system.txt"
        )

    async def execute(self, request: ExplanationRequest) -> ExplanationResponse:
        prompt_file = (
            self.prediction_prompt_file
            if isinstance(request, PredictionExplanationRequest)
            else self.optimization_prompt_file
        )

        user_prompt = json.dumps(
            request.model_dump(exclude_none=True),
            ensure_ascii=False,
        )

        # LLMClient 내부에서 ModelNotReadyException / ModelInferenceException 발생 가능
        llm_raw_text = await self.llm_client.chat_from_file(
            prompt_file=prompt_file,
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