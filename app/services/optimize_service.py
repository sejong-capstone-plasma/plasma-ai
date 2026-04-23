from app.core.exceptions import OptimizationException
from app.schemas.optimize import OptimizeRequest, OptimizeResponse


class OptimizeService:
    async def execute(self, request: OptimizeRequest) -> OptimizeResponse:
        raise OptimizationException(
            message="최적화 서비스가 아직 구현되지 않았습니다.",
            details={},
        )