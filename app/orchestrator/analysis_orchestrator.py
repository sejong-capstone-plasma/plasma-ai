from app.schemas.common import ExplanationContent
from app.schemas.pipelines import (
    ExtractPipelineResponse,
    OptimizationPipelineRequest,
    OptimizationPipelineResponse,
    PredictionPipelineRequest,
    PredictionPipelineResponse,
)
from app.schemas.explanation import (
    OptimizationExplanationRequest,
    PredictionExplanationRequest,
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

    async def run_extract_pipeline(
        self,
        request: ExtractParametersRequest,
    ) -> ExtractPipelineResponse:
        extract_response: ExtractParametersResponse = await self.extract_service.execute(request)

        return ExtractPipelineResponse(
            extract=extract_response,
        )

    async def run_prediction_pipeline(
        self,
        request: PredictionPipelineRequest,
    ) -> PredictionPipelineResponse:
        predict_request = PredictRequest(
            request_id=request.request_id,
            process_type=request.process_type,
            process_params=request.process_params,
        )
        predict_response: PredictResponse = self.predict_service.execute(predict_request)

        explanation_request = PredictionExplanationRequest(
            request_id=request.request_id,
            original_user_input=request.original_user_input,
            task_type="PREDICTION",
            process_type=request.process_type,
            process_params=request.process_params,
            prediction_result=predict_response.prediction_result,
        )
        explanation_response = await self.explanation_service.execute(explanation_request)

        return PredictionPipelineResponse(
            request_id=predict_response.request_id,
            process_type=predict_response.process_type,
            prediction_result=predict_response.prediction_result,
            explanation=ExplanationContent(
                summary=explanation_response.summary,
                details=explanation_response.details,
            ),
        )

    async def run_optimization_pipeline(
        self,
        request: OptimizationPipelineRequest,
    ) -> OptimizationPipelineResponse:
        optimize_request = OptimizeRequest(
            request_id=request.request_id,
            process_type=request.process_type,
            process_params=request.process_params,
        )
        optimization_response: OptimizeResponse = await self.optimize_service.execute(optimize_request)

        explanation_request = OptimizationExplanationRequest(
            request_id=request.request_id,
            original_user_input=request.original_user_input,
            task_type="OPTIMIZATION",
            process_type=request.process_type,
            process_params=request.process_params,
            current_outputs=request.current_outputs,
            baseline_outputs=optimization_response.baseline_outputs,
            optimization_result=optimization_response.optimization_result,
        )
        explanation_response = await self.explanation_service.execute(explanation_request)

        return OptimizationPipelineResponse(
            request_id=request.request_id,
            process_type=request.process_type,
            baseline_outputs=optimization_response.baseline_outputs,
            optimization_result=optimization_response.optimization_result,
            explanation=ExplanationContent(
                summary=explanation_response.summary,
                details=explanation_response.details,
            ),
        )