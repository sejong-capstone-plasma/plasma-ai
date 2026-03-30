from typing import List

from pydantic import BaseModel, Field

from app.core.enums import ProcessType, TaskType, ValidationStatus
from app.schemas.common import ProcessParams, TargetSpecs


class ExtractParametersRequest(BaseModel):
    request_id: str
    user_input: str = Field(..., description="Natural language process analysis request")


class ExtractParametersResponse(BaseModel):
    request_id: str
    task_type: TaskType
    process_type: ProcessType
    process_params: ProcessParams 
    target_specs: TargetSpecs
    validation_status: ValidationStatus
    missing_fields: List[str]