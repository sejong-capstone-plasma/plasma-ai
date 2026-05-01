from __future__ import annotations

import optuna

from app.domain.etch_score_calculator import EtchScoreCalculator
from app.models.predictor import IonPredictor, Predictor
from app.schemas.common import (
    ImprovementEvaluation,
    PredictionResult,
    ProcessParams,
    ValueWithUnit,
)
from app.schemas.optimize import OptimizationCandidate

optuna.logging.set_verbosity(optuna.logging.WARNING)

N_TRIALS = 200
N_CANDIDATES = 3
SEARCH_RATIO = 0.35  # ±35% around base values


class OptimizerRunner:
    def __init__(
        self,
        predictor: Predictor | None = None,
        etch_score_calculator: EtchScoreCalculator | None = None,
    ) -> None:
        self.predictor = predictor or IonPredictor()
        self.etch_score_calculator = etch_score_calculator or EtchScoreCalculator()

    def run(
        self, base_params: ProcessParams, base_etch_score: float
    ) -> list[OptimizationCandidate]:
        base_pressure = base_params.pressure.value
        base_source = base_params.source_power.value
        base_bias = base_params.bias_power.value

        def objective(trial: optuna.Trial) -> float:
            pressure = trial.suggest_float(
                "pressure",
                max(1.0, base_pressure * (1 - SEARCH_RATIO)),
                base_pressure * (1 + SEARCH_RATIO),
            )
            source_power = trial.suggest_float(
                "source_power",
                max(1.0, base_source * (1 - SEARCH_RATIO)),
                base_source * (1 + SEARCH_RATIO),
            )
            bias_power = trial.suggest_float(
                "bias_power",
                max(0.0, base_bias * (1 - SEARCH_RATIO)),
                base_bias * (1 + SEARCH_RATIO),
            )
            params = ProcessParams(
                pressure=ValueWithUnit(value=pressure, unit=base_params.pressure.unit),
                source_power=ValueWithUnit(value=source_power, unit=base_params.source_power.unit),
                bias_power=ValueWithUnit(value=bias_power, unit=base_params.bias_power.unit),
            )
            flux, energy = self.predictor.predict(params)
            etch_score = self.etch_score_calculator.calculate(flux, energy)

            trial.set_user_attr("flux", flux)
            trial.set_user_attr("energy", energy)
            trial.set_user_attr("etch_score", etch_score)
            return etch_score

        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=N_TRIALS)

        improved = [
            t for t in study.trials
            if t.value is not None and t.value > base_etch_score
        ]
        improved.sort(key=lambda t: t.value, reverse=True)  # type: ignore[arg-type]

        seen_scores: set[float] = set()
        unique_improved = []
        for trial in improved:
            score_key = round(trial.user_attrs["etch_score"], 2)
            if score_key not in seen_scores:
                seen_scores.add(score_key)
                unique_improved.append(trial)
            if len(unique_improved) == N_CANDIDATES:
                break

        candidates: list[OptimizationCandidate] = []
        for rank, trial in enumerate(unique_improved, start=1):
            p = trial.params
            etch_score = trial.user_attrs["etch_score"]
            flux = trial.user_attrs["flux"]
            energy = trial.user_attrs["energy"]

            increase_value = etch_score - base_etch_score
            increase_percent = (increase_value / base_etch_score * 100) if base_etch_score > 0 else 0.0

            candidates.append(
                OptimizationCandidate(
                    rank=rank,
                    process_params=ProcessParams(
                        pressure=ValueWithUnit(value=round(p["pressure"], 2), unit=base_params.pressure.unit),
                        source_power=ValueWithUnit(value=round(p["source_power"], 2), unit=base_params.source_power.unit),
                        bias_power=ValueWithUnit(value=round(p["bias_power"], 2), unit=base_params.bias_power.unit),
                    ),
                    prediction_result=PredictionResult(
                        ion_flux=ValueWithUnit(value=flux, unit="cm^-2 s^-1"),
                        ion_energy=ValueWithUnit(value=round(energy, 2), unit="eV"),
                        etch_score=ValueWithUnit(value=round(etch_score, 2), unit="point"),
                    ),
                    improvement_evaluation=ImprovementEvaluation(
                        increase_value=ValueWithUnit(value=round(increase_value, 2), unit="point"),
                        increase_percent=ValueWithUnit(value=round(increase_percent, 2), unit="%"),
                    ),
                    score=round(etch_score / 100.0, 3),
                )
            )

        return candidates
