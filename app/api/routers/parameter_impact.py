from fastapi import APIRouter

from app.schemas.parameter_impact import ParameterImpactRequest, ParameterImpactResponse
from app.services.parameter_impact_service import ParameterImpactService

router = APIRouter()
parameter_impact_service = ParameterImpactService()


@router.post("/parameter-impact", response_model=ParameterImpactResponse)
async def parameter_impact(request: ParameterImpactRequest) -> ParameterImpactResponse:
    return await parameter_impact_service.execute(request)
