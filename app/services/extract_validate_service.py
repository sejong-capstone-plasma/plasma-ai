from __future__ import annotations

from app.core.enums import FieldStatus
from app.domain.extraction_validator import ExtractionValidator
from app.schemas.common import ProcessParams, ValidatedProcessParams, ValidatedValueWithUnit
from app.schemas.extract import ExtractParametersResponse, ExtractValidateRequest


class ExtractValidateService:
    def __init__(
        self,
        extraction_validator: ExtractionValidator | None = None,
    ) -> None:
        self.extraction_validator = extraction_validator or ExtractionValidator()

    def execute(
        self,
        request: ExtractValidateRequest,
    ) -> ExtractParametersResponse:
        validated_process_params = self._to_validated_process_params(request.process_params)

        return self.extraction_validator.validate_and_normalize(
            request_id=request.request_id,
            task_type=request.task_type,
            process_type=request.process_type,
            process_params=validated_process_params,
            current_outputs=request.current_outputs,
        )

    def _to_validated_process_params(
        self,
        process_params: ProcessParams,
    ) -> ValidatedProcessParams:
        return ValidatedProcessParams(
            pressure=self._to_validated_value(process_params.pressure),
            source_power=self._to_validated_value(process_params.source_power),
            bias_power=self._to_validated_value(process_params.bias_power),
        )

    def _to_validated_value(
        self,
        item,
    ) -> ValidatedValueWithUnit:
        if item.value is None and item.unit is None:
            status = FieldStatus.MISSING
        elif item.value is None or item.unit is None:
            status = FieldStatus.AMBIGUOUS
        else:
            status = FieldStatus.VALID

        return ValidatedValueWithUnit(
            value=item.value,
            unit=item.unit,
            status=status,
        )