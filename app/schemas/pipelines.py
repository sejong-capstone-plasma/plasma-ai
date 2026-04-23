from pydantic import BaseModel, Field

from app.core.enums import ProcessType
from app.schemas.common import CommonBaseModel, ExplanationContent, PredictionResult, ProcessParams
from app.schemas.extract import ExtractParametersResponse
from app.schemas.predict import PredictResponse
from app.schemas.optimize import OptimizeResponse
from app.schemas.explanation import ExplanationResponse

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


class OptimizationPipelineResponse(BaseModel):
    current_prediction: PredictResponse
    optimization: OptimizeResponse
    explanation: ExplanationResponse