from __future__ import annotations

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

    Note: not yet implemented — returns UNSUPPORTED.
    """

    async def execute(
        self,
        request: ExtractParametersRequest,
        cleaned_input: str,
        history: list[dict[str, str]],
        task_type: TaskType,
        process_type: ProcessType,
    ) -> ExtractParametersResponse:
        return self._unsupported_response(request.request_id, task_type, process_type)
