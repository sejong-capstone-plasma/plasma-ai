from fastapi import APIRouter

from app.schemas.extract import ExtractParametersRequest, ExtractParametersResponse
from app.services.extract_service import ExtractService

router = APIRouter()
extract_service = ExtractService()


@router.post("/extract-parameters", response_model=ExtractParametersResponse)
def extract_parameters(request: ExtractParametersRequest) -> ExtractParametersResponse:
    return extract_service.execute(request)