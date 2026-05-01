from __future__ import annotations

import asyncio

from app.core.exceptions import AppException, ModelInferenceException, OptimizationException
from app.domain.etch_score_calculator import EtchScoreCalculator
from app.models.optimizer_runner import OptimizerRunner
from app.models.predictor import IonPredictor, Predictor
from app.schemas.common import BaselineOutputs, ValueWithUnit
from app.schemas.optimize import OptimizationResult, OptimizeRequest, OptimizeResponse


class OptimizeService:
    def __init__(
        self,
        predictor: Predictor | None = None,
        etch_score_calculator: EtchScoreCalculator | None = None,
    ) -> None:
        self.predictor = predictor or IonPredictor()
        self.etch_score_calculator = etch_score_calculator or EtchScoreCalculator()
        self.optimizer_runner = OptimizerRunner(self.predictor, self.etch_score_calculator)

    async def execute(self, request: OptimizeRequest) -> OptimizeResponse:
        base_params = request.process_params

        try:
            base_flux, base_energy = self.predictor.predict(base_params)
        except AppException:
            raise
        except Exception as e:
            raise ModelInferenceException(
                message="베이스라인 예측 중 오류가 발생했습니다.",
            ) from e

        base_etch_score = self.etch_score_calculator.calculate(base_flux, base_energy)

        try:
            candidates = await asyncio.to_thread(
                self.optimizer_runner.run, base_params, base_etch_score
            )
        except AppException:
            raise
        except Exception as e:
            raise OptimizationException(
                message="최적화 탐색 중 오류가 발생했습니다.",
                details={"error": str(e)},
            ) from e

        return OptimizeResponse(
            request_id=request.request_id,
            process_type=request.process_type,
            baseline_outputs=BaselineOutputs(
                etch_score=ValueWithUnit(value=round(base_etch_score, 2), unit="point"),
            ),
            optimization_result=OptimizationResult(
                candidate_count=len(candidates),
                optimization_candidates=candidates,
            ),
        )
