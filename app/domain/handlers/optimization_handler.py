from __future__ import annotations

from pathlib import Path

from app.core.enums import ProcessType, TaskType
from app.domain.handlers.base import BaseTaskHandler
from app.schemas.extract import ExtractParametersRequest, ExtractParametersResponse

_PROMPT_FILE = str(
    Path(__file__).resolve().parents[2] / "llm" / "prompts" / "extract_optimization.txt"
)


class OptimizationHandler(BaseTaskHandler):
    """
    Handles OPTIMIZATION task.

    Cases:
    - 2-1. Current utterance contains params → extract and validate
    - 2-2. No params in current utterance → resolve from history (LLM), or INVALID_FIELD if none
    - 2-3. Current utterance modifies history params → LLM applies delta, then validate
    """

    async def execute(
        self,
        request: ExtractParametersRequest,
        cleaned_input: str,
        history: list[dict[str, str]],
        task_type: TaskType,
        process_type: ProcessType,
    ) -> ExtractParametersResponse:
        raise NotImplementedError
