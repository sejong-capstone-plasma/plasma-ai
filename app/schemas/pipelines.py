from typing import Optional

from pydantic import BaseModel, Field

from app.core.enums import ProcessType
from app.schemas.common import (
    BaselineOutputs,
    CommonBaseModel,
    CurrentOutputs,
    ExplanationContent,
    PredictionResult,
    ProcessParams,
)
from app.schemas.extract import ExtractParametersResponse
from app.schemas.optimize import OptimizationResult


class ExtractPipelineResponse(BaseModel):
    extract: ExtractParametersResponse


class PredictionPipelineRequest(CommonBaseModel):
    request_id: str = Field(..., description="Request identifier")
    original_user_input: str = Field(..., description="Original user input text")
    process_type: ProcessType = Field(..., description="Process type")
    process_params: ProcessParams = Field(..., description="Confirmed process parameters")


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


class OptimizationPipelineResponse(CommonBaseModel):
    request_id: str
    process_type: ProcessType
    baseline_outputs: BaselineOutputs
    optimization_result: OptimizationResult
    explanation: ExplanationContent