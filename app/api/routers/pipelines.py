from fastapi import APIRouter

from app.orchestrator.analysis_orchestrator import AnalysisOrchestrator
from app.schemas.pipelines import (
    ExtractPipelineResponse,
    PredictionPipelineResponse,
    OptimizationPipelineResponse,
)
from app.schemas.extract import ExtractParametersRequest
from app.schemas.predict import PredictRequest
from app.schemas.optimize import OptimizeRequest

router = APIRouter()
analysis_orchestrator = AnalysisOrchestrator()


@router.post("/extract", response_model=ExtractPipelineResponse)
def run_extract(request: ExtractParametersRequest) -> ExtractPipelineResponse:
    return analysis_orchestrator.run_extract_pipeline(request)


@router.post("/predict", response_model=PredictionPipelineResponse)
def run_predict(request: PredictRequest) -> PredictionPipelineResponse:
    return analysis_orchestrator.run_prediction_pipeline(request)


@router.post("/optimize", response_model=OptimizationPipelineResponse)
def run_optimize(request: OptimizeRequest) -> OptimizationPipelineResponse:
    return analysis_orchestrator.run_optimization_pipeline(request)