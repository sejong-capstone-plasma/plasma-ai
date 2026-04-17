import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.enums import ErrorCode
from app.core.exceptions import AppException
from app.schemas.error import ErrorResponse

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException):
        logger.warning(
            "AppException: path=%s error_code=%s message=%s details=%s",
            request.url.path,
            exc.error_code,
            exc.message,
            exc.details,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error_code=exc.error_code.value,
                message=exc.message,
                details=exc.details,
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(request: Request, exc: RequestValidationError):
        logger.warning(
            "RequestValidationError: path=%s errors=%s",
            request.url.path,
            exc.errors(),
        )
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                error_code=ErrorCode.REQUEST_VALIDATION_ERROR.value,
                message="Request validation failed",
                details={"errors": exc.errors()},
            ).model_dump(),
        )

    @app.exception_handler(ValidationError)
    async def handle_validation_error(request: Request, exc: ValidationError):
        logger.warning(
            "ValidationError: path=%s errors=%s",
            request.url.path,
            exc.errors(),
        )
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                error_code=ErrorCode.REQUEST_VALIDATION_ERROR.value,
                message="Validation failed",
                details={"errors": exc.errors()},
            ).model_dump(),
        )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        logger.warning(
            "HTTPException: path=%s status=%s detail=%s",
            request.url.path,
            exc.status_code,
            exc.detail,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error_code=ErrorCode.INVALID_INPUT.value,
                message=str(exc.detail),
                details=None,
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(request: Request, exc: Exception):
        logger.exception("Unexpected exception: path=%s", request.url.path)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error_code=ErrorCode.INTERNAL_SERVER_ERROR.value,
                message="Unexpected server error",
                details=None,
            ).model_dump(),
        )