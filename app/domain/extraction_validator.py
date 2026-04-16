from __future__ import annotations

from typing import Any

from app.core.enums import FieldStatus, ProcessType, TaskType, ValidationStatus
from app.schemas.common import (
    CurrentOutputs,
    ValidatedProcessParams,
    ValidatedValueWithUnit,
    ValueWithUnit,
)
from app.schemas.extract import ExtractParametersResponse
from app.core.exceptions import ModelInferenceException

class ExtractionValidator:
    PRESSURE_MIN_MTORR = 0.0
    PRESSURE_MAX_MTORR = 1000.0

    POWER_MIN_W = 0.0
    POWER_MAX_W = 5000.0

    def validate_and_normalize(
        self,
        request_id: str,
        llm_output: dict[str, Any],
    ) -> ExtractParametersResponse:
        if not isinstance(llm_output, dict):
            raise ModelInferenceException(
                message="LLM 출력 형식이 올바르지 않습니다.",
                details={
                    "reason": "llm_output_must_be_object",
                    "actual_type": type(llm_output).__name__,
                },
            )


        task_type = self._parse_task_type(llm_output.get("task_type"))
        process_type = self._parse_process_type(llm_output.get("process_type"))

        process_params_raw = llm_output.get("process_params") or {}
        current_outputs_raw = llm_output.get("current_outputs")

        if process_params_raw is not None and not isinstance(process_params_raw, dict):
            raise ModelInferenceException(
                message="LLM 출력의 process_params 형식이 올바르지 않습니다.",
                details={"reason": "process_params_must_be_object"},
            )

        if current_outputs_raw is not None and not isinstance(current_outputs_raw, dict):
            raise ModelInferenceException(
                message="LLM 출력의 current_outputs 형식이 올바르지 않습니다.",
                details={"reason": "current_outputs_must_be_object"},
            )

        process_params = ValidatedProcessParams(
            pressure=self._parse_process_field(process_params_raw.get("pressure")),
            source_power=self._parse_process_field(process_params_raw.get("source_power")),
            bias_power=self._parse_process_field(process_params_raw.get("bias_power")),
        )

        process_params = self._normalize_process_params(process_params)
        current_outputs = self._parse_current_outputs(current_outputs_raw)

        validation_status = self._determine_validation_status(
            task_type=task_type,
            process_type=process_type,
            process_params=process_params,
        )

        return ExtractParametersResponse(
            request_id=request_id,
            validation_status=validation_status,
            process_type=process_type,
            task_type=task_type,
            process_params=process_params,
            current_outputs=current_outputs,
        )

    def _parse_task_type(self, raw: Any) -> TaskType:
        try:
            return TaskType(raw)
        except Exception:
            return TaskType.UNSUPPORTED

    def _parse_process_type(self, raw: Any) -> ProcessType:
        try:
            return ProcessType(raw)
        except Exception:
            return ProcessType.UNKNOWN

    def _parse_status_hint(self, raw: Any) -> FieldStatus:
        if raw == FieldStatus.VALID.value:
            return FieldStatus.VALID
        if raw == FieldStatus.MISSING.value:
            return FieldStatus.MISSING
        if raw == FieldStatus.AMBIGUOUS.value:
            return FieldStatus.AMBIGUOUS
        if raw == FieldStatus.OUT_OF_RANGE.value:
            return FieldStatus.OUT_OF_RANGE
        return FieldStatus.AMBIGUOUS

    def _parse_process_field(self, raw: Any) -> ValidatedValueWithUnit:
        if not isinstance(raw, dict):
            return ValidatedValueWithUnit(
                value=None,
                unit=None,
                status=FieldStatus.MISSING,
            )

        value = self._safe_float(raw.get("value"))
        unit = raw.get("unit") if isinstance(raw.get("unit"), str) else None
        status_hint = raw.get("status_hint", raw.get("status"))
        status = self._parse_status_hint(status_hint)

        # 1차 방어: 값/단위 존재 여부 기준으로 최소 보정
        if value is None and unit is None:
            status = FieldStatus.MISSING
        elif value is None or unit is None:
            status = FieldStatus.AMBIGUOUS

        return ValidatedValueWithUnit(
            value=value,
            unit=unit,
            status=status,
        )

    def _parse_current_outputs(self, raw: Any) -> CurrentOutputs | None:
        if not isinstance(raw, dict):
            return None

        etch_rate_raw = raw.get("etch_rate")
        etch_rate = self._parse_output_field(etch_rate_raw)
        if etch_rate is None:
            return None

        return CurrentOutputs(etch_rate=etch_rate)

    def _parse_output_field(self, raw: Any) -> ValueWithUnit | None:
        if not isinstance(raw, dict):
            return None

        value = self._safe_float(raw.get("value"))
        unit = raw.get("unit") if isinstance(raw.get("unit"), str) else None

        if value is None or unit is None:
            return None

        normalized = self._normalize_output_value(value=value, unit=unit)
        if normalized is None:
            return None

        return ValueWithUnit(value=normalized["value"], unit=normalized["unit"])

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

    def _normalize_output_value(self, value: float, unit: str) -> dict[str, float | str] | None:
        unit_norm = self._normalize_unit_text(unit)

        if unit_norm == "nm/min":
            return {"value": value, "unit": "nm/min"}

        if unit_norm in {"um/min", "μm/min", "µm/min"}:
            return {"value": value * 1000.0, "unit": "nm/min"}

        return None

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

    @staticmethod
    def _safe_float(value: Any) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None