from fastapi import APIRouter

from app.api.routers import health, extract, pipelines, predict, optimize, explanation


api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(extract.router, prefix="/ai/services", tags=["services"])
api_router.include_router(predict.router, prefix="/ai/services", tags=["services"])
api_router.include_router(optimize.router, prefix="/ai/services", tags=["services"])
api_router.include_router(explanation.router, prefix="/ai/services", tags=["services"])

api_router.include_router(pipelines.router, prefix="/ai/pipelines", tags=["pipelines"])