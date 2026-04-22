from __future__ import annotations

from pydantic import Field

from app.core.enums import ProcessType
from app.schemas.common import CommonBaseModel, PredictionResult, ProcessParams


class PredictRequest(CommonBaseModel):
    request_id: str = Field(..., description="Request identifier")
    process_type: ProcessType = Field(..., description="Process type")
    process_params: ProcessParams = Field(..., description="Confirmed process parameters")


class PredictResponse(CommonBaseModel):
    request_id: str = Field(..., description="Request identifier")
    process_type: ProcessType = Field(..., description="Process type")
    prediction_result: PredictionResult = Field(..., description="Model prediction output")
