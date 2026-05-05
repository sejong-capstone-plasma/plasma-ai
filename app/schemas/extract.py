from typing import List, Literal

from pydantic import Field

from app.core.enums import ProcessType, TaskType, ValidationStatus
from app.schemas.common import CommonBaseModel, CurrentOutputs, ProcessParams, ValidatedProcessParams


class ChatMessage(CommonBaseModel):
    role: Literal["user", "assistant"] = Field(..., description="Message role")
    content: str = Field(..., description="Message content")


class ExtractParametersRequest(CommonBaseModel):
    request_id: str = Field(..., description="Request identifier")
    user_input: str = Field(..., description="Natural language process analysis request")
    history: List[ChatMessage] = Field(default_factory=list, description="Previous conversation history")


class ExtractParametersResponse(CommonBaseModel):
    request_id: str = Field(..., description="Request identifier")
    validation_status: ValidationStatus = Field(..., description="Overall validation status")
    process_type: ProcessType = Field(..., description="Detected process type")
    task_type: TaskType = Field(..., description="Detected task type")
    process_params: ValidatedProcessParams | None = Field(
        default=None,
        description="Extracted and validated process parameters (PREDICTION/OPTIMIZATION only)"
    )
    current_outputs: CurrentOutputs | None = Field(
        default=None,
        description="Optional current output values extracted from user input"
    )
    condition_a: ValidatedProcessParams | None = Field(
        default=None,
        description="First condition (COMPARISON only)"
    )
    condition_b: ValidatedProcessParams | None = Field(
        default=None,
        description="Second condition (COMPARISON only)"
    )

class ExtractValidateRequest(CommonBaseModel):
    request_id: str = Field(..., description="Request identifier")
    process_type: ProcessType = Field(..., description="Process type")
    task_type: TaskType = Field(..., description="Task type")
    process_params: ProcessParams | None = Field(
        default=None,
        description="Structured process parameters from backend (PREDICTION/OPTIMIZATION only)"
    )
    current_outputs: CurrentOutputs | None = Field(
        default=None,
        description="Optional current output values"
    )
    condition_a: ProcessParams | None = Field(
        default=None,
        description="First condition (COMPARISON only)"
    )
    condition_b: ProcessParams | None = Field(
        default=None,
        description="Second condition (COMPARISON only)"
    )