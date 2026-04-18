from fastapi import APIRouter

from app.schemas.extract import ExtractValidateRequest, ExtractParametersResponse
from app.services.extract_validate_service import ExtractValidateService

router = APIRouter()
service = ExtractValidateService()


@router.post("/ai/extract-validate", response_model=ExtractParametersResponse)
async def validate_extract(request: ExtractValidateRequest) -> ExtractParametersResponse:
    return service.execute(request)