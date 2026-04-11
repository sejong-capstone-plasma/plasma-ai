from typing import List, Literal, Union

from pydantic import BaseModel

from app.schemas.common import ProcessParams
from app.schemas.optimize import OptimizationCandidate


class PredictionExplanationRequest(BaseModel):
    request_id: str
    task_type: Literal["PREDICTION"]
    process_params: ProcessParams
    result: str


class OptimizationExplanationRequest(BaseModel):
    request_id: str
    task_type: Literal["OPTIMIZATION"]
    process_params: ProcessParams
    target_specs: str
    result: List[OptimizationCandidate]


ExplanationRequest = Union[
    PredictionExplanationRequest,
    OptimizationExplanationRequest,
]


class ExplanationResponse(BaseModel):
    request_id: str
    summary: str
    details: List[str]