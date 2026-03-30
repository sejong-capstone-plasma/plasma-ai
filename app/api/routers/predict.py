from fastapi import APIRouter

from app.schemas.predict import PredictRequest, PredictResponse
from app.services.predict_service import PredictService

router = APIRouter()
predict_service = PredictService()


@router.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    return predict_service.execute(request)