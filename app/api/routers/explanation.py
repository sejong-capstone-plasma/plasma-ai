from fastapi import APIRouter

from app.schemas.explanation import ExplanationRequest, ExplanationResponse
from app.services.explanation_service import ExplanationService

router = APIRouter()
explanation_service = ExplanationService()


@router.post("/generate-explanation", response_model=ExplanationResponse)
def generate_explanation(request: ExplanationRequest) -> ExplanationResponse:
    return explanation_service.execute(request)