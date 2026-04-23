from typing import Annotated, List, Literal, Optional, Union

from pydantic import Field

from app.core.enums import ProcessType
from app.schemas.common import (
    BaselineOutputs,
    CommonBaseModel,
    CurrentOutputs,
    ProcessParams,
    PredictionResult,
)
from app.schemas.optimize import OptimizationResult


class PredictionExplanationRequest(CommonBaseModel):
    request_id: str
    original_user_input: str
    task_type: Literal["PREDICTION"]
    process_type: ProcessType
    process_params: ProcessParams
    current_outputs: Optional[CurrentOutputs] = None
    prediction_result: PredictionResult


class OptimizationExplanationRequest(CommonBaseModel):
    request_id: str
    original_user_input: str
    task_type: Literal["OPTIMIZATION"]
    process_type: ProcessType
    process_params: ProcessParams
    current_outputs: Optional[CurrentOutputs] = None
    baseline_outputs: BaselineOutputs
    optimization_result: OptimizationResult


GenerateExplanationRequest = Annotated[
    Union[PredictionExplanationRequest, OptimizationExplanationRequest],
    Field(discriminator="task_type"),
]

ExplanationRequest = GenerateExplanationRequest


class ExplanationResponse(CommonBaseModel):
    request_id: str
    summary: str
    details: List[str]


GenerateExplanationResponse = ExplanationResponse