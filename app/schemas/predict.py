from pydantic import BaseModel

from app.schemas.common import ProcessParams, ResultParams


class PredictRequest(BaseModel):
    request_id: str
    process_params: ProcessParams


class PredictResponse(BaseModel):
    request_id: str
    prediction_result: ResultParams