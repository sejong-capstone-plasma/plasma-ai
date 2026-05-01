import math

import pytest

from app.models.optimizer_runner import OptimizerRunner
from app.schemas.common import ProcessParams, ValueWithUnit


BASE_PARAMS = ProcessParams(
    pressure=ValueWithUnit(value=20.0, unit="mTorr"),
    source_power=ValueWithUnit(value=600.0, unit="W"),
    bias_power=ValueWithUnit(value=100.0, unit="W"),
)


class ScalablePredictor:
    """Flux/energy proportional to params — optimizer can always find improvements."""

    def predict(self, params: ProcessParams) -> tuple[float, float]:
        flux = params.source_power.value * 1e12 / params.pressure.value
        energy = params.bias_power.value * 0.2 + 15.0
        return flux, energy


class ConstantPredictor:
    """Always returns the same values — optimizer cannot improve."""

    def __init__(self, flux: float = 1e15, energy: float = 25.0) -> None:
        self._flux = flux
        self._energy = energy

    def predict(self, params: ProcessParams) -> tuple[float, float]:
        return self._flux, self._energy


class SimpleEtchScoreCalculator:
    P5: float = 0.0
    P95: float = 7.867448e17

    def calculate(self, ion_flux: float, ion_energy: float) -> float:
        raw = ion_flux * math.sqrt(max(ion_energy - 20.0, 0.0))
        normalized = (raw - self.P5) / (self.P95 - self.P5) * 100.0
        return max(0.0, min(100.0, normalized))


def _base_score(predictor, calculator) -> float:
    flux, energy = predictor.predict(BASE_PARAMS)
    return calculator.calculate(flux, energy)


def test_candidates_all_exceed_baseline():
    predictor = ScalablePredictor()
    calculator = SimpleEtchScoreCalculator()
    base_score = _base_score(predictor, calculator)

    runner = OptimizerRunner(predictor=predictor, etch_score_calculator=calculator)
    candidates = runner.run(BASE_PARAMS, base_score)

    assert len(candidates) > 0
    for c in candidates:
        assert c.prediction_result.etch_score.value > base_score


def test_candidates_count_at_most_three():
    predictor = ScalablePredictor()
    calculator = SimpleEtchScoreCalculator()
    base_score = _base_score(predictor, calculator)

    runner = OptimizerRunner(predictor=predictor, etch_score_calculator=calculator)
    candidates = runner.run(BASE_PARAMS, base_score)

    assert len(candidates) <= 3


def test_candidates_ranked_by_etch_score_descending():
    predictor = ScalablePredictor()
    calculator = SimpleEtchScoreCalculator()
    base_score = _base_score(predictor, calculator)

    runner = OptimizerRunner(predictor=predictor, etch_score_calculator=calculator)
    candidates = runner.run(BASE_PARAMS, base_score)

    scores = [c.prediction_result.etch_score.value for c in candidates]
    assert scores == sorted(scores, reverse=True)


def test_candidate_ranks_are_sequential():
    predictor = ScalablePredictor()
    calculator = SimpleEtchScoreCalculator()
    base_score = _base_score(predictor, calculator)

    runner = OptimizerRunner(predictor=predictor, etch_score_calculator=calculator)
    candidates = runner.run(BASE_PARAMS, base_score)

    ranks = [c.rank for c in candidates]
    assert ranks == list(range(1, len(candidates) + 1))


def test_improvement_evaluation_is_consistent():
    predictor = ScalablePredictor()
    calculator = SimpleEtchScoreCalculator()
    base_score = _base_score(predictor, calculator)

    runner = OptimizerRunner(predictor=predictor, etch_score_calculator=calculator)
    candidates = runner.run(BASE_PARAMS, base_score)

    for c in candidates:
        inc_val = c.improvement_evaluation.increase_value.value
        inc_pct = c.improvement_evaluation.increase_percent.value

        # 증가량/퍼센트 모두 양수
        assert inc_val > 0
        assert inc_pct > 0

        # 단위
        assert c.improvement_evaluation.increase_value.unit == "point"
        assert c.improvement_evaluation.increase_percent.unit == "%"

        # 저장된 increase_value 기준으로 increase_percent 일관성 확인 (10% 상대 오차 허용)
        expected_pct = inc_val / base_score * 100
        assert inc_pct == pytest.approx(expected_pct, rel=0.1)


def test_score_field_is_normalized():
    predictor = ScalablePredictor()
    calculator = SimpleEtchScoreCalculator()
    base_score = _base_score(predictor, calculator)

    runner = OptimizerRunner(predictor=predictor, etch_score_calculator=calculator)
    candidates = runner.run(BASE_PARAMS, base_score)

    for c in candidates:
        assert 0.0 <= c.score <= 1.0


def test_returns_empty_when_no_improvement():
    calculator = SimpleEtchScoreCalculator()
    flux, energy = ConstantPredictor().predict(BASE_PARAMS)
    base_score = calculator.calculate(flux, energy)

    runner = OptimizerRunner(predictor=ConstantPredictor(), etch_score_calculator=calculator)
    candidates = runner.run(BASE_PARAMS, base_score)

    assert candidates == []


def test_process_params_units_preserved():
    predictor = ScalablePredictor()
    calculator = SimpleEtchScoreCalculator()
    base_score = _base_score(predictor, calculator)

    runner = OptimizerRunner(predictor=predictor, etch_score_calculator=calculator)
    candidates = runner.run(BASE_PARAMS, base_score)

    for c in candidates:
        assert c.process_params.pressure.unit == "mTorr"
        assert c.process_params.source_power.unit == "W"
        assert c.process_params.bias_power.unit == "W"
