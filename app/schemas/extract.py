from pydantic import BaseModel, Field

from app.core.enums import ProcessType, TaskType, ValidationStatus
from app.schemas.common import ValidatedEtchRateOutput, ValidatedProcessParams


class ExtractParametersRequest(BaseModel):
    request_id: str = Field(..., description="Request identifier")
    user_input: str = Field(..., description="Natural language process analysis request")


class ExtractParametersResponse(BaseModel):
    request_id: str = Field(..., description="Request identifier")
    validation_status: ValidationStatus = Field(..., description="Overall validation status")
    process_type: ProcessType = Field(..., description="Detected process type")
    task_type: TaskType = Field(..., description="Detected task type")
    process_params: ValidatedProcessParams = Field(
        ...,
        description="Extracted and validated process parameters"
    )
    current_outputs: ValidatedEtchRateOutput | None = Field(
        default=None,
        description="Optional current output values extracted from user input"
    )