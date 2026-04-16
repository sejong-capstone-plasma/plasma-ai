from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    success: bool = Field(default=False)
    error_code: str
    message: str
    details: dict[str, Any] | None = None