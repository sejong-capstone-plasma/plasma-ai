from __future__ import annotations

from app.core.enums import ProcessType, TaskType, ValidationStatus
from app.domain.handlers.base import BaseTaskHandler
from app.schemas.extract import ExtractParametersRequest, ExtractParametersResponse


class QuestionHandler(BaseTaskHandler):
    """
    Handles QUESTION task.

    No parameter extraction needed — questions are answered directly by the
    downstream pipeline using the original user input and conversation history.
    """

    async def execute(
        self,
        request: ExtractParametersRequest,
        cleaned_input: str,
        history: list[dict[str, str]],
        task_type: TaskType,
        process_type: ProcessType,
    ) -> ExtractParametersResponse:
        return ExtractParametersResponse(
            request_id=request.request_id,
            validation_status=ValidationStatus.VALID,
            task_type=task_type,
            process_type=process_type,
            process_params=None,
            current_outputs=None,
        )
