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
    process_params: ValidatedProcessParams = Field(
        ...,
        description="Extracted and validated process parameters"
    )
    current_outputs: CurrentOutputs | None = Field(
        default=None,
        description="Optional current output values extracted from user input"
    )

class ExtractValidateRequest(CommonBaseModel):
    request_id: str = Field(..., description="Request identifier")
    process_type: ProcessType = Field(..., description="Process type")
    task_type: TaskType = Field(..., description="Task type")
    process_params: ProcessParams = Field(
        ...,
        description="Structured process parameters from backend"
    )
    current_outputs: CurrentOutputs | None = Field(
        default=None,
        description="Optional current output values"
    )