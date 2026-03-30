from app.core.enums import GoalType
from app.schemas.common import ValueWithUnit
from app.schemas.optimize import (
    OptimizeRequest,
    OptimizeResponse,
    OptimizationCandidate,
    GoalEvaluation,
    GoalEvaluationItem,
)


class OptimizeService:
    def execute(self, request: OptimizeRequest) -> OptimizeResponse:
        return OptimizeResponse(
            request_id=request.request_id,
            optimization_candidates=[
                OptimizationCandidate(
                    rank=1,
                    process_params={
                        "pressure_mtorr": ValueWithUnit(value=18.5, unit="mTorr"),
                        "source_power_w": ValueWithUnit(value=520, unit="W"),
                        "bias_power_w": ValueWithUnit(value=185, unit="W"),
                    },
                    predicted_outputs={
                        "ion_density_cm3": ValueWithUnit(value=1.02e11, unit="/cm3"),
                        "ion_temp_ev": ValueWithUnit(value=3.95, unit="eV"),
                    },
                    goal_evaluation=GoalEvaluation(
                        ion_density_cm3=GoalEvaluationItem(
                            goal_type=GoalType.EXACT,
                            target_value=1.00e11,
                            difference=2.0e9,
                        ),
                        ion_temp_ev=GoalEvaluationItem(
                            goal_type=GoalType.EXACT,
                            target_value=4.00,
                            difference=-0.05,
                        ),
                    ),
                    score=0.964,
                ),
                OptimizationCandidate(
                    rank=2,
                    process_params={
                        "pressure_mtorr": ValueWithUnit(value=19.0, unit="mTorr"),
                        "source_power_w": ValueWithUnit(value=510, unit="W"),
                        "bias_power_w": ValueWithUnit(value=190, unit="W"),
                    },
                    predicted_outputs={
                        "ion_density_cm3": ValueWithUnit(value=1.01e11, unit="/cm3"),
                        "ion_temp_ev": ValueWithUnit(value=3.90, unit="eV"),
                    },
                    goal_evaluation=GoalEvaluation(
                        ion_density_cm3=GoalEvaluationItem(
                            goal_type=GoalType.EXACT,
                            target_value=1.00e11,
                            difference=1.0e9,
                        ),
                        ion_temp_ev=GoalEvaluationItem(
                            goal_type=GoalType.EXACT,
                            target_value=4.00,
                            difference=-0.10,
                        ),
                    ),
                    score=0.951,
                ),
                OptimizationCandidate(
                    rank=3,
                    process_params={
                        "pressure_mtorr": ValueWithUnit(value=18.0, unit="mTorr"),
                        "source_power_w": ValueWithUnit(value=530, unit="W"),
                        "bias_power_w": ValueWithUnit(value=180, unit="W"),
                    },
                    predicted_outputs={
                        "ion_density_cm3": ValueWithUnit(value=1.03e11, unit="/cm3"),
                        "ion_temp_ev": ValueWithUnit(value=4.08, unit="eV"),
                    },
                    goal_evaluation=GoalEvaluation(
                        ion_density_cm3=GoalEvaluationItem(
                            goal_type=GoalType.EXACT,
                            target_value=1.00e11,
                            difference=3.0e9,
                        ),
                        ion_temp_ev=GoalEvaluationItem(
                            goal_type=GoalType.EXACT,
                            target_value=4.00,
                            difference=0.08,
                        ),
                    ),
                    score=0.944,
                ),
            ],
        )