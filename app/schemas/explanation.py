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
from app.schemas.extract import ChatMessage
from app.schemas.optimize import OptimizationResult


class PredictionExplanationRequest(CommonBaseModel):
    request_id: str
    original_user_input: str
    task_type: Literal["PREDICTION"]
    process_type: ProcessType
    process_params: ProcessParams
    current_outputs: Optional[CurrentOutputs] = None
    prediction_result: PredictionResult
    history: List[ChatMessage] = Field(default_factory=list)


class OptimizationExplanationRequest(CommonBaseModel):
    request_id: str
    original_user_input: str
    task_type: Literal["OPTIMIZATION"]
    process_type: ProcessType
    process_params: ProcessParams
    current_outputs: Optional[CurrentOutputs] = None
    baseline_outputs: BaselineOutputs
    optimization_result: OptimizationResult
    history: List[ChatMessage] = Field(default_factory=list)


class ComparisonConditionData(CommonBaseModel):
    process_params: ProcessParams
    prediction_result: PredictionResult


class ComparisonExplanationRequest(CommonBaseModel):
    request_id: str
    original_user_input: str
    task_type: Literal["COMPARISON"]
    process_type: ProcessType
    condition_a: ComparisonConditionData
    condition_b: ComparisonConditionData
    history: List[ChatMessage] = Field(default_factory=list)


GenerateExplanationRequest = Annotated[
    Union[
        PredictionExplanationRequest,
        OptimizationExplanationRequest,
        ComparisonExplanationRequest,
    ],
    Field(discriminator="task_type"),
]

ExplanationRequest = GenerateExplanationRequest


class ExplanationResponse(CommonBaseModel):
    request_id: str
    summary: str
    interpretation: dict


GenerateExplanationResponse = ExplanationResponse