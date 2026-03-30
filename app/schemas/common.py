from typing import Optional

from pydantic import BaseModel, Field

from app.core.enums import GoalType


class ValueWithUnit(BaseModel):
    value: float = Field(..., description="Numeric value")
    unit: str = Field(..., description="Unit string")

class GoalSpec(BaseModel):
    goal_type: GoalType = Field(..., description="Goal type")
    target_value: Optional[float] = Field(None, description="Target value for exact/min/max")
    unit: str = Field(..., description="Unit string")
    #min_value: Optional[float] = Field(None, description="Minimum value for range")
    #max_value: Optional[float] = Field(None, description="Maximum value for range")

class ProcessParams(BaseModel):
    pressure_mtorr: ValueWithUnit
    source_power_w: ValueWithUnit
    bias_power_w: ValueWithUnit

class ResultParams(BaseModel):
    ion_density_cm3: ValueWithUnit
    ion_temp_ev: ValueWithUnit

class TargetSpecs(BaseModel):
    ion_density_cm3: GoalSpec
    ion_temp_ev: GoalSpec