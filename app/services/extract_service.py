from __future__ import annotations

import json
from pathlib import Path

from app.domain.extraction_validator import ExtractionValidator
from app.domain.input_preprocessor import InputPreprocessor
from app.llm.client import LLMClient
from app.schemas.extract import ExtractParametersRequest, ExtractParametersResponse


class ExtractService:
    def __init__(
        self,
        llm_client: LLMClient | None = None,
        input_preprocessor: InputPreprocessor | None = None,
        extraction_validator: ExtractionValidator | None = None,
        prompt_file: str | None = None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()
        self.input_preprocessor = input_preprocessor or InputPreprocessor()
        self.extraction_validator = extraction_validator or ExtractionValidator()

        self.prompt_file = prompt_file or str(
            Path(__file__).resolve().parents[1] / "llm" / "prompts" / "extract_system.txt"
        )

    async def execute(
        self,
        request: ExtractParametersRequest,
    ) -> ExtractParametersResponse:
        # 1) 입력 전처리
        cleaned_input = self.input_preprocessor.clean(request.user_input)

        # 2) LLM user prompt 구성
        llm_user_prompt = json.dumps(
            {
                "request_id": request.request_id,
                "user_input": cleaned_input,
            },
            ensure_ascii=False,
        )

        # 3) LLM 호출
        llm_raw_text = await self.llm_client.chat_from_file(
            prompt_file=self.prompt_file,
            user_prompt=llm_user_prompt,
        )

        # 4) LLM 응답 JSON 파싱
        llm_output = self.llm_client.extract_json(llm_raw_text)

        # 5) 검증 / 정규화 + 최종 응답 생성
        return self.extraction_validator.validate_and_normalize(
            request_id=request.request_id,
            llm_output=llm_output,
        )