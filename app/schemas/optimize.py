from typing import List

from app.core.enums import ProcessType
from app.schemas.common import (
    BaselineOutputs,
    CommonBaseModel,
    ImprovementEvaluation,
    ProcessParams,
    PredictionResult,
)


class OptimizationCandidate(CommonBaseModel):
    rank: int
    process_params: ProcessParams
    prediction_result: PredictionResult
    improvement_evaluation: ImprovementEvaluation
    score: float


class OptimizationResult(CommonBaseModel):
    candidate_count: int
    optimization_candidates: List[OptimizationCandidate]


class OptimizeRequest(CommonBaseModel):
    request_id: str
    process_type: ProcessType
    process_params: ProcessParams


class OptimizeResponse(CommonBaseModel):
    request_id: str
    process_type: ProcessType
    baseline_outputs: BaselineOutputs
    optimization_result: OptimizationResult