from __future__ import annotations

from app.core.enums import FieldStatus, ProcessType, TaskType, ValidationStatus
from app.schemas.common import (
    CurrentOutputs,
    ValidatedProcessParams,
    ValidatedValueWithUnit,
)
from app.schemas.extract import ExtractParametersResponse


class ExtractionValidator:
    PRESSURE_MIN_MTORR = 0.0
    PRESSURE_MAX_MTORR = 1000.0

    POWER_MIN_W = 0.0
    POWER_MAX_W = 5000.0

    def validate_and_normalize(
        self,
        request_id: str,
        task_type: TaskType,
        process_type: ProcessType,
        process_params: ValidatedProcessParams,
        current_outputs: CurrentOutputs | None = None,
    ) -> ExtractParametersResponse:
        normalized_process_params = self._normalize_process_params(process_params)

        validation_status = self._determine_validation_status(
            task_type=task_type,
            process_type=process_type,
            process_params=normalized_process_params,
        )

        return ExtractParametersResponse(
            request_id=request_id,
            validation_status=validation_status,
            process_type=process_type,
            task_type=task_type,
            process_params=normalized_process_params,
            current_outputs=current_outputs,
        )

    def _normalize_process_params(
        self,
        process_params: ValidatedProcessParams,
    ) -> ValidatedProcessParams:
        return ValidatedProcessParams(
            pressure=self._normalize_pressure(process_params.pressure),
            source_power=self._normalize_power(process_params.source_power),
            bias_power=self._normalize_power(process_params.bias_power),
        )

    def _normalize_pressure(self, item: ValidatedValueWithUnit) -> ValidatedValueWithUnit:
        if item.value is None and item.unit is None:
            return self._with_status(item, FieldStatus.MISSING)

        if item.value is None or item.unit is None:
            return self._with_status(item, FieldStatus.AMBIGUOUS)

        unit_norm = self._normalize_unit_text(item.unit)

        if unit_norm == "mtorr":
            value_mtorr = item.value
        elif unit_norm == "torr":
            value_mtorr = item.value * 1000.0
        else:
            return ValidatedValueWithUnit(
                value=item.value,
                unit=item.unit,
                status=FieldStatus.AMBIGUOUS,
            )

        status = self._range_status(
            value=value_mtorr,
            min_value=self.PRESSURE_MIN_MTORR,
            max_value=self.PRESSURE_MAX_MTORR,
        )

        return ValidatedValueWithUnit(
            value=value_mtorr,
            unit="mTorr",
            status=status,
        )

    def _normalize_power(self, item: ValidatedValueWithUnit) -> ValidatedValueWithUnit:
        if item.value is None and item.unit is None:
            return self._with_status(item, FieldStatus.MISSING)

        if item.value is None or item.unit is None:
            return self._with_status(item, FieldStatus.AMBIGUOUS)

        unit_norm = self._normalize_unit_text(item.unit)

        if unit_norm == "w":
            value_w = item.value
        elif unit_norm == "kw":
            value_w = item.value * 1000.0
        else:
            return ValidatedValueWithUnit(
                value=item.value,
                unit=item.unit,
                status=FieldStatus.AMBIGUOUS,
            )

        status = self._range_status(
            value=value_w,
            min_value=self.POWER_MIN_W,
            max_value=self.POWER_MAX_W,
        )

        return ValidatedValueWithUnit(
            value=value_w,
            unit="W",
            status=status,
        )

    def _determine_validation_status(
        self,
        task_type: TaskType,
        process_type: ProcessType,
        process_params: ValidatedProcessParams,
    ) -> ValidationStatus:
        if task_type == TaskType.UNSUPPORTED or process_type == ProcessType.UNKNOWN:
            return ValidationStatus.UNSUPPORTED

        required_fields = [
            process_params.pressure,
            process_params.source_power,
            process_params.bias_power,
        ]

        if all(field.status == FieldStatus.VALID for field in required_fields):
            return ValidationStatus.VALID

        return ValidationStatus.INVALID_FIELD

    def _range_status(
        self,
        value: float,
        min_value: float,
        max_value: float,
    ) -> FieldStatus:
        if min_value <= value <= max_value:
            return FieldStatus.VALID
        return FieldStatus.OUT_OF_RANGE

    def _with_status(
        self,
        item: ValidatedValueWithUnit,
        status: FieldStatus,
    ) -> ValidatedValueWithUnit:
        return ValidatedValueWithUnit(
            value=item.value,
            unit=item.unit,
            status=status,
        )

    @staticmethod
    def _normalize_unit_text(unit: str) -> str:
        return unit.strip().lower().replace(" ", "")