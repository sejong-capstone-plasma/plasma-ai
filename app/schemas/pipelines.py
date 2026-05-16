from typing import List, Optional

from pydantic import BaseModel, Field

from app.core.enums import ProcessType
from app.schemas.common import (
    BaselineOutputs,
    CommonBaseModel,
    ConditionResult,
    CurrentOutputs,
    ExplanationContent,
    PredictionResult,
    ProcessParams,
)
from app.schemas.extract import ChatMessage, ExtractParametersResponse
from app.schemas.optimize import OptimizationResult


class ExtractPipelineResponse(BaseModel):
    extract: ExtractParametersResponse


class PredictionPipelineRequest(CommonBaseModel):
    request_id: str = Field(..., description="Request identifier")
    original_user_input: str = Field(..., description="Original user input text")
    process_type: ProcessType = Field(..., description="Process type")
    process_params: ProcessParams = Field(..., description="Confirmed process parameters")
    history: List[ChatMessage] = Field(default_factory=list, description="Conversation history")


class PredictionPipelineResponse(CommonBaseModel):
    request_id: str
    process_type: ProcessType
    prediction_result: PredictionResult
    explanation: ExplanationContent


class OptimizationPipelineRequest(CommonBaseModel):
    request_id: str = Field(..., description="Request identifier")
    original_user_input: str = Field(..., description="Original user input text")
    process_type: ProcessType = Field(..., description="Process type")
    process_params: ProcessParams = Field(..., description="Confirmed process parameters")
    current_outputs: Optional[CurrentOutputs] = Field(default=None, description="Current output values provided by user")
    history: List[ChatMessage] = Field(default_factory=list, description="Conversation history")


class OptimizationPipelineResponse(CommonBaseModel):
    request_id: str
    process_type: ProcessType
    baseline_outputs: BaselineOutputs
    optimization_result: OptimizationResult
    explanation: ExplanationContent


class ComparisonPipelineRequest(CommonBaseModel):
    request_id: str = Field(..., description="Request identifier")
    original_user_input: str = Field(..., description="Original user input text")
    process_type: ProcessType = Field(..., description="Process type")
    condition_a: ProcessParams = Field(..., description="First condition")
    condition_b: ProcessParams = Field(..., description="Second condition")
    history: List[ChatMessage] = Field(default_factory=list, description="Conversation history")


class ComparisonPipelineResponse(CommonBaseModel):
    request_id: str
    process_type: ProcessType
    condition_a: ConditionResult
    condition_b: ConditionResult
    explanation: ExplanationContent


# Question pipeline schemas are defined in schemas/question.py
from app.schemas.question import QuestionPipelineRequest as QuestionPipelineRequest  # noqa: E402
from app.schemas.question import QuestionPipelineResponse as QuestionPipelineResponse  # noqa: E402
