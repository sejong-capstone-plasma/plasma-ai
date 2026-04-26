from typing import List

from pydantic import BaseModel, Field, ConfigDict

from app.core.enums import FieldStatus


class CommonBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ValueWithUnit(CommonBaseModel):
    value: float = Field(..., description="Numeric value")
    unit: str = Field(..., description="Unit string")


class ValidatedValueWithUnit(CommonBaseModel):
    value: float | None = Field(default=None, description="Numeric value")
    unit: str | None = Field(default=None, description="Unit string")
    status: FieldStatus = Field(..., description="Field validation status")


class ProcessParams(CommonBaseModel):
    pressure: ValueWithUnit
    source_power: ValueWithUnit
    bias_power: ValueWithUnit


class ValidatedProcessParams(CommonBaseModel):
    pressure: ValidatedValueWithUnit
    source_power: ValidatedValueWithUnit
    bias_power: ValidatedValueWithUnit


class CurrentOutputs(CommonBaseModel):
    etch_rate: ValueWithUnit


class PredictionResult(CommonBaseModel):
    ion_flux: ValueWithUnit
    ion_energy: ValueWithUnit
    etch_score: ValueWithUnit


class BaselineOutputs(CommonBaseModel):
    etch_score: ValueWithUnit


class ImprovementEvaluation(CommonBaseModel):
    increase_value: ValueWithUnit
    increase_percent: ValueWithUnit


class ExplanationContent(CommonBaseModel):
    summary: str
    details: List[str]