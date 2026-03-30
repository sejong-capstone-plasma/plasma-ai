from app.schemas.pipelines import (
    ExtractPipelineResponse,
    PredictionPipelineResponse,
    OptimizationPipelineResponse,
)
from app.schemas.explanation import (
    PredictionExplanationRequest,
    OptimizationExplanationRequest,
)
from app.schemas.extract import (
    ExtractParametersRequest,
    ExtractParametersResponse,
)
from app.schemas.optimize import (
    OptimizeRequest,
    OptimizeResponse,
)
from app.schemas.predict import (
    PredictRequest,
    PredictResponse,
)
from app.services.explanation_service import ExplanationService
from app.services.extract_service import ExtractService
from app.services.optimize_service import OptimizeService
from app.services.predict_service import PredictService


class AnalysisOrchestrator:
    def __init__(self) -> None:
        self.extract_service = ExtractService()
        self.predict_service = PredictService()
        self.optimize_service = OptimizeService()
        self.explanation_service = ExplanationService()

    def run_extract_pipeline(
        self,
        request: ExtractParametersRequest,
    ) -> ExtractPipelineResponse:
        extract_response: ExtractParametersResponse = self.extract_service.execute(request)

        return ExtractPipelineResponse(
            extract=extract_response,
        )

    def run_prediction_pipeline(
        self,
        request: PredictRequest,
    ) -> PredictionPipelineResponse:
        prediction_response: PredictResponse = self.predict_service.execute(request)

        explanation_request = PredictionExplanationRequest(
            request_id=request.request_id,
            task_type="PREDICTION",
            process_params=request.process_params,
            result=prediction_response.prediction_result,
        )
        explanation_response = self.explanation_service.execute(explanation_request)

        return PredictionPipelineResponse(
            prediction=prediction_response,
            explanation=explanation_response,
        )

    def run_optimization_pipeline(
        self,
        request: OptimizeRequest,
    ) -> OptimizationPipelineResponse:
        # 1) 현재 조건 기준 예측 먼저 수행
        prediction_request = PredictRequest(
            request_id=request.request_id,
            process_params=request.process_params,
        )
        current_prediction: PredictResponse = self.predict_service.execute(prediction_request)

        # 2) 그 다음 최적화 수행
        optimization_response: OptimizeResponse = self.optimize_service.execute(request)

        # 3) 최적화 결과 설명 생성
        explanation_request = OptimizationExplanationRequest(
            request_id=request.request_id,
            task_type="OPTIMIZATION",
            process_params=request.process_params,
            target_specs=request.target_specs,
            result=optimization_response.optimization_candidates,
        )
        explanation_response = self.explanation_service.execute(explanation_request)

        return OptimizationPipelineResponse(
            current_prediction=current_prediction,
            optimization=optimization_response,
            explanation=explanation_response,
        )