from __future__ import annotations

from typing import Any

from app.core.enums import FieldStatus, ProcessType, TaskType
from app.core.exceptions import ModelInferenceException
from app.schemas.common import (
    CurrentOutputs,
    ValidatedProcessParams,
    ValidatedValueWithUnit,
    ValueWithUnit,
)


class LLMExtractionParser:
    def parse(
        self,
        llm_output: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(llm_output, dict):
            raise ModelInferenceException(
                message="LLM 출력 형식이 올바르지 않습니다.",
                details={
                    "reason": "llm_output_must_be_object",
                    "actual_type": type(llm_output).__name__,
                },
            )

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

        return {
            "task_type": self._parse_task_type(llm_output.get("task_type")),
            "process_type": self._parse_process_type(llm_output.get("process_type")),
            "process_params": ValidatedProcessParams(
                pressure=self._parse_process_field(process_params_raw.get("pressure")),
                source_power=self._parse_process_field(process_params_raw.get("source_power")),
                bias_power=self._parse_process_field(process_params_raw.get("bias_power")),
            ),
            "current_outputs": self._parse_current_outputs(current_outputs_raw),
        }

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

        unit_norm = self._normalize_unit_text(unit)

        if unit_norm == "nm/min":
            return ValueWithUnit(value=value, unit="nm/min")

        if unit_norm in {"um/min", "μm/min", "µm/min"}:
            return ValueWithUnit(value=value * 1000.0, unit="nm/min")

        return None

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