from __future__ import annotations

from pathlib import Path

import pandas as pd
from joblib import load

from app.core.config import settings
from app.schemas.common import ProcessParams


def _add_physics_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["source_per_pressure"] = df["source_power_w"] / df["pressure_mtorr"]
    df["bias_per_pressure"]   = df["bias_power_w"]   / df["pressure_mtorr"]
    return df


class Predictor:
    def predict(self, process_params: ProcessParams) -> tuple[float, float]:
        """
        Returns:
            (ion_flux [cm^-2 s^-1], ion_energy [eV])
        """
        raise NotImplementedError


class IonPredictor(Predictor):
    """XGBoost 기반 이온 플럭스 / 에너지 예측기."""

    MODEL_FILENAME = "xgb_ion_models.joblib"

    def __init__(self, model_path: str | Path | None = None) -> None:
        self._model_path = Path(model_path) if model_path else settings.model_dir / self.MODEL_FILENAME
        self._loaded                  = False
        self._flux_model              = None
        self._energy_model_on         = None
        self._energy_model_off        = None
        self._flux_feature_cols       = None
        self._energy_on_feature_cols  = None
        self._energy_off_feature_cols = None
        self._train_stats             = None

    def _load(self) -> None:
        from app.core.exceptions import ModelNotReadyException
        try:
            bundle = load(self._model_path)
        except FileNotFoundError:
            raise ModelNotReadyException(
                message="모델 파일을 찾을 수 없습니다.",
                details={"path": str(self._model_path)},
            )
        self._flux_model              = bundle["flux_model"]
        self._energy_model_on         = bundle["energy_model_on"]
        self._energy_model_off        = bundle["energy_model_off"]
        self._flux_feature_cols       = bundle["flux_feature_cols"]
        self._energy_on_feature_cols  = bundle["energy_on_feature_cols"]
        self._energy_off_feature_cols = bundle["energy_off_feature_cols"]
        self._train_stats             = bundle["train_stats"]
        self._loaded                  = True

    def predict(self, process_params: ProcessParams) -> tuple[float, float]:
        if not self._loaded:
            self._load()

        pressure_mtorr = process_params.pressure.value
        source_power_w = process_params.source_power.value
        bias_power_w   = process_params.bias_power.value

        row = pd.DataFrame([{
            "pressure_mtorr": pressure_mtorr,
            "source_power_w": source_power_w,
            "bias_power_w"  : bias_power_w,
        }])
        row_ext = _add_physics_features(row)

        flux_log = self._flux_model.predict(row_ext[self._flux_feature_cols])[0]

        if bias_power_w > 0:
            energy = self._energy_model_on.predict(row_ext[self._energy_on_feature_cols])[0]
        else:
            energy = self._energy_model_off.predict(row_ext[self._energy_off_feature_cols])[0]

        return float(10 ** flux_log), float(energy)
