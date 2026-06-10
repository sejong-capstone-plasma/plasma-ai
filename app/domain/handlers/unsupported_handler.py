from __future__ import annotations

from app.core.enums import FieldStatus, ProcessType, TaskType, ValidationStatus
from app.domain.handlers.base import BaseTaskHandler
from app.schemas.common import ValidatedProcessParams, ValidatedValueWithUnit
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
        resolved_task_type = TaskType.QUESTION if process_type == ProcessType.ETCH else task_type
        empty = ValidatedValueWithUnit(value=None, unit=None, status=FieldStatus.MISSING)

        return ExtractParametersResponse(
            request_id=request.request_id,
            validation_status=ValidationStatus.UNSUPPORTED,
            task_type=resolved_task_type,
            process_type=process_type,
            process_params=ValidatedProcessParams(
                pressure=empty,
                source_power=empty,
                bias_power=empty,
            ),
            current_outputs=None,
        )
