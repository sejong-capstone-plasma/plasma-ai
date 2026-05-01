from __future__ import annotations

from app.core.enums import ProcessType, TaskType
from app.domain.handlers.base import BaseTaskHandler
from app.schemas.extract import ExtractParametersRequest, ExtractParametersResponse


class UnsupportedHandler(BaseTaskHandler):
    async def execute(
        self,
        request: ExtractParametersRequest,
        cleaned_input: str,
        history: list[dict[str, str]],
        task_type: TaskType,
        process_type: ProcessType,
    ) -> ExtractParametersResponse:
        return self._unsupported_response(request.request_id, task_type, process_type)
