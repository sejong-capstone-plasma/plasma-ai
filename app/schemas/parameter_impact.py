from typing import List

from app.core.enums import ProcessType
from app.schemas.common import CommonBaseModel, ProcessParams


class ImpactPoint(CommonBaseModel):
    x: float
    y: float


class ParameterImpactRequest(CommonBaseModel):
    request_id: str
    process_type: ProcessType
    process_params: ProcessParams


class ParameterImpactResponse(CommonBaseModel):
    request_id: str
    process_type: ProcessType
    pressure_impact: List[ImpactPoint]
    source_power_impact: List[ImpactPoint]
    bias_power_impact: List[ImpactPoint]
