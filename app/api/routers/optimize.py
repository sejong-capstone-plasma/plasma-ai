from fastapi import APIRouter

from app.schemas.optimize import OptimizeRequest, OptimizeResponse
from app.services.optimize_service import OptimizeService

router = APIRouter()
optimize_service = OptimizeService()


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize(request: OptimizeRequest) -> OptimizeResponse:
    return await optimize_service.execute(request)