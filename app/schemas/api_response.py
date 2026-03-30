from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "ok"
    data: Optional[T] = None


class SimpleMessageResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict[str, Any]] = None