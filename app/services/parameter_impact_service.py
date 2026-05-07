from __future__ import annotations

import asyncio

import numpy as np

from app.core.exceptions import AppException, ModelInferenceException
from app.domain.etch_score_calculator import EtchScoreCalculator
from app.models.predictor import IonPredictor, Predictor
from app.schemas.common import ProcessParams, ValueWithUnit
from app.schemas.parameter_impact import ImpactPoint, ParameterImpactRequest, ParameterImpactResponse


class ParameterImpactService:
    NUM_POINTS = 50

    PRESSURE_MIN = 2.0
    PRESSURE_MAX = 10.0
    SOURCE_POWER_MIN = 100.0
    SOURCE_POWER_MAX = 500.0
    BIAS_POWER_MIN = 0.0
    BIAS_POWER_MAX = 1000.0

    def __init__(
        self,
        predictor: Predictor | None = None,
        etch_score_calculator: EtchScoreCalculator | None = None,
    ) -> None:
        self.predictor = predictor or IonPredictor()
        self.etch_score_calculator = etch_score_calculator or EtchScoreCalculator()

    async def execute(self, request: ParameterImpactRequest) -> ParameterImpactResponse:
        base = request.process_params

        try:
            pressure_impact, source_power_impact, bias_power_impact = await asyncio.to_thread(
                self._compute_all, base
            )
        except AppException:
            raise
        except Exception as e:
            raise ModelInferenceException(
                message="파라미터 영향 분석 중 오류가 발생했습니다.",
            ) from e

        return ParameterImpactResponse(
            request_id=request.request_id,
            process_type=request.process_type,
            pressure_impact=pressure_impact,
            source_power_impact=source_power_impact,
            bias_power_impact=bias_power_impact,
        )

    def _compute_all(
        self, base: ProcessParams
    ) -> tuple[list[ImpactPoint], list[ImpactPoint], list[ImpactPoint]]:
        return (
            self._sweep_pressure(base),
            self._sweep_source_power(base),
            self._sweep_bias_power(base),
        )

    def _sweep_pressure(self, base: ProcessParams) -> list[ImpactPoint]:
        return [
            self._compute_point(
                ProcessParams(
                    pressure=ValueWithUnit(value=v, unit="mTorr"),
                    source_power=base.source_power,
                    bias_power=base.bias_power,
                ),
                x=v,
            )
            for v in np.linspace(self.PRESSURE_MIN, self.PRESSURE_MAX, self.NUM_POINTS)
        ]

    def _sweep_source_power(self, base: ProcessParams) -> list[ImpactPoint]:
        return [
            self._compute_point(
                ProcessParams(
                    pressure=base.pressure,
                    source_power=ValueWithUnit(value=v, unit="W"),
                    bias_power=base.bias_power,
                ),
                x=v,
            )
            for v in np.linspace(self.SOURCE_POWER_MIN, self.SOURCE_POWER_MAX, self.NUM_POINTS)
        ]

    def _sweep_bias_power(self, base: ProcessParams) -> list[ImpactPoint]:
        return [
            self._compute_point(
                ProcessParams(
                    pressure=base.pressure,
                    source_power=base.source_power,
                    bias_power=ValueWithUnit(value=v, unit="W"),
                ),
                x=v,
            )
            for v in np.linspace(self.BIAS_POWER_MIN, self.BIAS_POWER_MAX, self.NUM_POINTS)
        ]

    def _compute_point(self, params: ProcessParams, x: float) -> ImpactPoint:
        flux, energy = self.predictor.predict(params)
        score = self.etch_score_calculator.calculate(flux, energy)
        return ImpactPoint(x=round(float(x), 4), y=round(score, 2))
