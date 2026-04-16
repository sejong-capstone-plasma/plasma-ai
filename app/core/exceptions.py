from typing import Any

from app.core.enums import ErrorCode


class AppException(Exception):
    error_code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR
    status_code: int = 500

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        error_code: ErrorCode | None = None,
        status_code: int | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.error_code = error_code or self.__class__.error_code
        self.status_code = status_code or self.__class__.status_code


class ValidationException(AppException):
    error_code = ErrorCode.INVALID_INPUT
    status_code = 400


class MissingRequiredFieldException(AppException):
    error_code = ErrorCode.MISSING_REQUIRED_FIELD
    status_code = 400


class UnsupportedTaskException(AppException):
    error_code = ErrorCode.UNSUPPORTED_TASK
    status_code = 400


class AmbiguousRequestException(AppException):
    error_code = ErrorCode.AMBIGUOUS_REQUEST
    status_code = 400


class ModelNotReadyException(AppException):
    error_code = ErrorCode.MODEL_NOT_READY
    status_code = 503


class ModelInferenceException(AppException):
    error_code = ErrorCode.MODEL_INFERENCE_FAILED
    status_code = 500


class OptimizationException(AppException):
    error_code = ErrorCode.OPTIMIZATION_FAILED
    status_code = 500