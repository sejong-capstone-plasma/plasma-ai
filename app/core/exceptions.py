class AppException(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        status_code: int = 400,
        details: dict | None = None,
    ):
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class ValidationException(AppException):
    pass


class UnsupportedTaskException(AppException):
    pass


class AmbiguousRequestException(AppException):
    pass


class ModelInferenceException(AppException):
    pass


class OptimizationException(AppException):
    pass