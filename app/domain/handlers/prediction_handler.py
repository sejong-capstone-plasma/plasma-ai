from __future__ import annotations

import json
from pathlib import Path

from app.core.enums import ProcessType, TaskType
from app.domain.handlers.base import BaseTaskHandler
from app.schemas.extract import ExtractParametersRequest, ExtractParametersResponse

_PROMPT_FILE = str(
    Path(__file__).resolve().parents[2] / "llm" / "prompts" / "extract_prediction.txt"
)


class PredictionHandler(BaseTaskHandler):
    """
    Handles PREDICTION task.

    Cases:
    - 1-1. Current utterance contains params → extract and validate
    - 1-2. No params in current utterance → resolve from history (LLM), or INVALID_FIELD if none
    - 1-3. Current utterance modifies history params → LLM applies delta, then validate
    """

    async def execute(
        self,
        request: ExtractParametersRequest,
        cleaned_input: str,
        history: list[dict[str, str]],
        task_type: TaskType,
        process_type: ProcessType,
    ) -> ExtractParametersResponse:
        extract_user_prompt = json.dumps(
            {
                "request_id": request.request_id,
                "user_input": cleaned_input,
            },
            ensure_ascii=False,
        )
        extract_raw = await self.llm_client.chat_with_history_from_file(
            prompt_file=_PROMPT_FILE,
            history=history,
            user_prompt=extract_user_prompt,
        )
        extract_output = self.llm_client.extract_json(extract_raw)
        extract_parsed = self.llm_extraction_parser.parse(extract_output)

        return self.extraction_validator.validate_and_normalize(
            request_id=request.request_id,
            task_type=task_type,
            process_type=process_type,
            process_params=extract_parsed["process_params"],
            current_outputs=extract_parsed["current_outputs"],
        )
