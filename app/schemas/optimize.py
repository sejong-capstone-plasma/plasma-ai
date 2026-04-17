from typing import List

from pydantic import BaseModel

from app.schemas.common import ProcessParams


class GoalEvaluationItem(BaseModel):
    goal_type: str
    target_value: float
    difference: float

class GoalEvaluation(BaseModel):
    ion_density_cm3: GoalEvaluationItem
    ion_temp_ev: GoalEvaluationItem 

class OptimizationCandidate(BaseModel):
    rank: int
    process_params: ProcessParams
    predicted_outputs: str
    goal_evaluation: GoalEvaluation
    score: float


class OptimizeRequest(BaseModel):
    request_id: str
    process_params: ProcessParams
    target_specs: str


class OptimizeResponse(BaseModel):
    request_id: str
    optimization_candidates: List[OptimizationCandidate]