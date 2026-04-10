from pydantic import BaseModel, Field

from app.core.enums import FieldStatus


class ValueWithUnit(BaseModel):
    value: float = Field(..., description="Numeric value")
    unit: str = Field(..., description="Unit string")

class ValidatedValueWithUnit(BaseModel):
    value: float | None = Field(default=None, description="Numeric value")
    unit: str | None = Field(default=None, description="Unit string")
    status: FieldStatus = Field(..., description="Field validation status")
    
class ProcessParams(BaseModel):
    pressure: ValueWithUnit
    source_power: ValueWithUnit
    bias_power: ValueWithUnit

class ValidatedProcessParams(BaseModel):
    pressure: ValidatedValueWithUnit
    source_power: ValidatedValueWithUnit
    bias_power: ValidatedValueWithUnit
    
class ImprovementEvaluation(BaseModel):
    increase_value: ValueWithUnit
    increase_percent: ValueWithUnit

class EtchRateOutput(BaseModel):
    etch_rate: ValueWithUnit

class ValidatedEtchRateOutput(BaseModel):
    etch_rate: ValidatedValueWithUnit