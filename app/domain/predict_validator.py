from __future__ import annotations

from app.core.enums import ProcessType
from app.core.exceptions import ValidationException
from app.schemas.common import ProcessParams
from app.schemas.predict import PredictRequest


class PredictValidator:
    SUPPORTED_PROCESSES: frozenset[ProcessType] = frozenset({ProcessType.ETCH})

    EXPECTED_UNITS: dict[str, str] = {
        "pressure": "mTorr",
        "source_power": "W",
        "bias_power": "W",
    }

    PARAM_BOUNDS: dict[str, tuple[float, float]] = {
        "pressure": (2.0, 10.0),
        "source_power": (100.0, 500.0),
        "bias_power": (0.0, 1000.0),
    }

    def validate(self, request: PredictRequest) -> None:
        self._validate_process_type(request.process_type)
        self._validate_units(request.process_params)
        self._validate_range(request.process_params)

    def _validate_process_type(self, process_type: ProcessType) -> None:
        if process_type not in self.SUPPORTED_PROCESSES:
            raise ValidationException(
                message=f"지원하지 않는 공정 유형입니다: '{process_type.value}'",
                details={
                    "process_type": process_type.value,
                    "supported": [p.value for p in self.SUPPORTED_PROCESSES],
                },
            )

    def _validate_units(self, params: ProcessParams) -> None:
        fields = {
            "pressure": params.pressure.unit,
            "source_power": params.source_power.unit,
            "bias_power": params.bias_power.unit,
        }
        violations = [
            f"'{name}': 단위 '{unit}' (기대값: '{self.EXPECTED_UNITS[name]}')"
            for name, unit in fields.items()
            if unit != self.EXPECTED_UNITS[name]
        ]
        if violations:
            raise ValidationException(
                message="단위가 올바르지 않습니다:\n" + "\n".join(violations),
                details={"violations": violations},
            )

    def _validate_range(self, params: ProcessParams) -> None:
        fields = {
            "pressure": params.pressure.value,
            "source_power": params.source_power.value,
            "bias_power": params.bias_power.value,
        }
        violations = []
        for name, val in fields.items():
            lo, hi = self.PARAM_BOUNDS[name]
            if not (lo <= val <= hi):
                violations.append(f"'{name}' = {val} (허용 범위: [{lo}, {hi}])")
        if violations:
            raise ValidationException(
                message="입력값이 허용 범위를 벗어났습니다:\n" + "\n".join(violations),
                details={"violations": violations},
            )
