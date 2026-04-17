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
            
        )