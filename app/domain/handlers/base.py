from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.enums import FieldStatus, ProcessType, TaskType, ValidationStatus
from app.domain.extraction_validator import ExtractionValidator
from app.domain.llm_extraction_parser import LLMExtractionParser
from app.llm.client import LLMClient
from app.schemas.common import ValidatedProcessParams, ValidatedValueWithUnit
from app.schemas.extract import ExtractParametersRequest, ExtractParametersResponse


class BaseTaskHandler(ABC):
    def __init__(
        self,
        llm_client: LLMClient,
        llm_extraction_parser: LLMExtractionParser,
        extraction_validator: ExtractionValidator,
    ) -> None:
        self.llm_client = llm_client
        self.llm_extraction_parser = llm_extraction_parser
        self.extraction_validator = extraction_validator

    @abstractmethod
    async def execute(
        self,
        request: ExtractParametersRequest,
        cleaned_input: str,
        history: list[dict[str, str]],
        task_type: TaskType,
        process_type: ProcessType,
    ) -> ExtractParametersResponse:
        ...

    def _unsupported_response(
        self,
        request_id: str,
        task_type: TaskType,
        process_type: ProcessType,
    ) -> ExtractParametersResponse:
        empty = ValidatedValueWithUnit(value=None, unit=None, status=FieldStatus.MISSING)
        return ExtractParametersResponse(
            request_id=request_id,
            validation_status=ValidationStatus.UNSUPPORTED,
            task_type=task_type,
            process_type=process_type,
            process_params=ValidatedProcessParams(
                pressure=empty,
                source_power=empty,
                bias_power=empty,
            ),
            current_outputs=None,
        )
