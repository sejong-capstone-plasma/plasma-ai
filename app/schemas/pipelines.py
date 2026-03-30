from pydantic import BaseModel

from app.schemas.extract import ExtractParametersResponse
from app.schemas.predict import PredictResponse
from app.schemas.optimize import OptimizeResponse
from app.schemas.explanation import ExplanationResponse


class ExtractPipelineResponse(BaseModel):
    extract: ExtractParametersResponse


class PredictionPipelineResponse(BaseModel):
    prediction: PredictResponse
    explanation: ExplanationResponse


class OptimizationPipelineResponse(BaseModel):
    current_prediction: PredictResponse
    optimization: OptimizeResponse
    explanation: ExplanationResponse