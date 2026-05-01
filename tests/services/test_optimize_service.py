import pytest

from app.core.enums import ProcessType
from app.core.exceptions import OptimizationException
from app.schemas.common import (
    ImprovementEvaluation,
    PredictionResult,
    ProcessParams,
    ValueWithUnit,
)
from app.schemas.optimize import OptimizationCandidate, OptimizeRequest
from app.services.optimize_service import OptimizeService


BASE_PARAMS = ProcessParams(
    pressure=ValueWithUnit(value=20.0, unit="mTorr"),
    source_power=ValueWithUnit(value=600.0, unit="W"),
    bias_power=ValueWithUnit(value=100.0, unit="W"),
)

CANDIDATE = OptimizationCandidate(
    rank=1,
    process_params=ProcessParams(
        pressure=ValueWithUnit(value=18.5, unit="mTorr"),
        source_power=ValueWithUnit(value=620.0, unit="W"),
        bias_power=ValueWithUnit(value=90.0, unit="W"),
    ),
    prediction_result=PredictionResult(
        ion_flux=ValueWithUnit(value=7.4e15, unit="cm^-2 s^-1"),
        ion_energy=ValueWithUnit(value=17.9, unit="eV"),
        etch_score=ValueWithUnit(value=85.0, unit="point"),
    ),
    improvement_evaluation=ImprovementEvaluation(
        increase_value=ValueWithUnit(value=5.0, unit="point"),
        increase_percent=ValueWithUnit(value=6.25, unit="%"),
    ),
    score=0.85,
)


class FakePredictor:
    def predict(self, params: ProcessParams) -> tuple[float, float]:
        return 1e15, 25.0


class FakeEtchScoreCalculator:
    def calculate(self, ion_flux: float, ion_energy: float) -> float:
        return 80.0


class FakeOptimizerRunner:
    def __init__(self, candidates: list):
        self.called_with = None
        self._candidates = candidates

    def run(self, base_params: ProcessParams, base_etch_score: float) -> list:
        self.called_with = {"base_params": base_params, "base_etch_score": base_etch_score}
        return self._candidates


def _make_service(candidates: list) -> tuple[OptimizeService, FakeOptimizerRunner]:
    predictor = FakePredictor()
    calculator = FakeEtchScoreCalculator()
    runner = FakeOptimizerRunner(candidates)

    service = OptimizeService(predictor=predictor, etch_score_calculator=calculator)
    service.optimizer_runner = runner
    return service, runner


@pytest.mark.asyncio
async def test_execute_returns_correct_response_structure():
    service, runner = _make_service([CANDIDATE])

    request = OptimizeRequest(
        request_id="req-001",
        process_type=ProcessType.ETCH,
        process_params=BASE_PARAMS,
    )
    response = await service.execute(request)

    assert response.request_id == "req-001"
    assert response.process_type == ProcessType.ETCH
    assert response.baseline_outputs.etch_score.value == 80.0
    assert response.baseline_outputs.etch_score.unit == "point"
    assert response.optimization_result.candidate_count == 1
    assert response.optimization_result.optimization_candidates[0] == CANDIDATE


@pytest.mark.asyncio
async def test_execute_passes_baseline_to_runner():
    service, runner = _make_service([])

    request = OptimizeRequest(
        request_id="req-002",
        process_type=ProcessType.ETCH,
        process_params=BASE_PARAMS,
    )
    await service.execute(request)

    assert runner.called_with["base_etch_score"] == 80.0
    assert runner.called_with["base_params"] == BASE_PARAMS


@pytest.mark.asyncio
async def test_execute_returns_empty_candidates_when_no_improvement():
    service, _ = _make_service([])

    request = OptimizeRequest(
        request_id="req-003",
        process_type=ProcessType.ETCH,
        process_params=BASE_PARAMS,
    )
    response = await service.execute(request)

    assert response.optimization_result.candidate_count == 0
    assert response.optimization_result.optimization_candidates == []


@pytest.mark.asyncio
async def test_execute_raises_optimization_exception_on_runner_error():
    class BrokenOptimizerRunner:
        def run(self, base_params, base_etch_score):
            raise RuntimeError("optuna internal error")

    service, _ = _make_service([])
    service.optimizer_runner = BrokenOptimizerRunner()

    request = OptimizeRequest(
        request_id="req-004",
        process_type=ProcessType.ETCH,
        process_params=BASE_PARAMS,
    )

    with pytest.raises(OptimizationException):
        await service.execute(request)
