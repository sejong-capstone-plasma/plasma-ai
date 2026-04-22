from __future__ import annotations

from app.core.exceptions import AppException, ModelInferenceException, ValidationException
from app.domain.etch_score_calculator import EtchScoreCalculator
from app.models.predictor import IonPredictor, Predictor
from app.schemas.common import PredictionResult, ValueWithUnit
from app.schemas.predict import PredictRequest, PredictResponse


class PredictService:
    def __init__(
        self,
        predictor: Predictor | None = None,
        etch_score_calculator: EtchScoreCalculator | None = None,
    ) -> None:
        self.predictor = predictor or IonPredictor()
        self.etch_score_calculator = etch_score_calculator or EtchScoreCalculator()

    def execute(self, request: PredictRequest) -> PredictResponse:
        try:
            ion_flux, ion_energy = self.predictor.predict(request.process_params)
        except AppException:
            raise
        except ValueError as e:
            raise ValidationException(message=str(e)) from e
        except Exception as e:
            raise ModelInferenceException(message="모델 추론 중 오류가 발생했습니다.") from e

        etch_score = self.etch_score_calculator.calculate(ion_flux, ion_energy)

        return PredictResponse(
            request_id=request.request_id,
            process_type=request.process_type,
            prediction_result=PredictionResult(
                ion_flux=ValueWithUnit(value=ion_flux, unit="cm^-2 s^-1"),
                ion_energy=ValueWithUnit(value=ion_energy, unit="eV"),
                etch_score=ValueWithUnit(value=etch_score, unit="point"),
            ),
        )
