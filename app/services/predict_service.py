from app.schemas.predict import PredictRequest, PredictResponse
from app.schemas.common import ValueWithUnit


class PredictService:
    def execute(self, request: PredictRequest) -> PredictResponse:
        return PredictResponse(
            request_id=request.request_id,
            prediction_result={
                "ion_density_cm3": ValueWithUnit(value=4.32e11, unit="/cm3"),
                "ion_temp_ev": ValueWithUnit(value=3.1, unit="eV"),
            },
        )