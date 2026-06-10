from __future__ import annotations

import json
from pathlib import Path

from app.core.enums import ProcessType, TaskType
from app.domain.handlers.base import BaseTaskHandler
from app.schemas.extract import ExtractParametersRequest, ExtractParametersResponse

_PROMPT_FILE = str(
    Path(__file__).resolve().parents[2] / "llm" / "prompts" / "extract_comparison.txt"
)


class ComparisonHandler(BaseTaskHandler):
    """
    Handles COMPARISON task.

    Cases:
    - 3-1. No conditions in current utterance → resolve 2 conditions from history, or INVALID_FIELD if insufficient
    - 3-2. One condition in current utterance → combine with one from history, or INVALID_FIELD if missing
    - 3-3. Both conditions in current utterance → extract both directly
    - 3-4. Current utterance modifies a history condition → LLM applies delta to produce condition_b
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
            max_tokens=512,
        )
        extract_output = self.llm_client.extract_json(extract_raw)
        parsed = self.llm_extraction_parser.parse_comparison(extract_output)

        return self.extraction_validator.validate_comparison(
            request_id=request.request_id,
            process_type=process_type,
            condition_a_params=parsed["condition_a"],
            condition_b_params=parsed["condition_b"],
        )
