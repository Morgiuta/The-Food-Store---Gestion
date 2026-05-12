"""
Global exception handlers for RFC 7807-compliant error responses.
"""

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.core.exceptions import (
    AppException,
    ErrorResponse,
)

logger = logging.getLogger(__name__)


def register_error_handlers(app: FastAPI) -> None:
    """
    Register all custom exception handlers on the FastAPI app.

    Args:
        app: The FastAPI application instance
    """

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        """
        Handle custom AppException subclasses with RFC 7807 format.
        """
        logger.warning(
            f"AppException: {exc.status_code} | {exc.title} | {exc.detail}",
            extra={
                "status_code": exc.status_code,
                "title": exc.title,
                "detail": exc.detail,
                "path": str(request.url.path),
                "method": request.method,
            },
        )

        response = ErrorResponse(
            type=exc.exception_type,
            title=exc.title,
            status=exc.status_code,
            detail=exc.detail,
            instance=str(request.url.path),
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump(),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        """
        Handle standard HTTP exceptions with RFC 7807 format.
        """
        logger.warning(
            f"HTTPException: {exc.status_code} | {exc.detail}",
            extra={
                "status_code": exc.status_code,
                "detail": exc.detail,
                "path": str(request.url.path),
            },
        )

        response = ErrorResponse(
            type="about:blank",
            title=_get_status_title(exc.status_code),
            status=exc.status_code,
            detail=str(exc.detail),
            instance=str(request.url.path),
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """
        Handle Pydantic validation errors with RFC 7807 format.
        """
        errors = exc.errors()
        detail = "; ".join(
            f"{'.'.join(str(e) for e in error.get('loc', []))}: {error.get('msg', '')}"
            for error in errors
        )

        logger.warning(
            f"ValidationError: {detail}",
            extra={
                "path": str(request.url.path),
                "errors": errors,
            },
        )

        response = ErrorResponse(
            type="https://fastapi.tiangolo.com/errors/validation-error",
            title="Validation Error",
            status=422,
            detail=detail or "Request validation failed",
            instance=str(request.url.path),
        )

        return JSONResponse(
            status_code=422,
            content=response.model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """
        Catch-all for unhandled exceptions (500 Internal Server Error).
        """
        logger.exception(
            f"Unhandled exception: {str(exc)}",
            extra={
                "path": str(request.url.path),
                "method": request.method,
            },
        )

        response = ErrorResponse(
            type="about:blank",
            title="Internal Server Error",
            status=500,
            detail="An unexpected error occurred. Please try again later.",
            instance=str(request.url.path),
        )

        return JSONResponse(
            status_code=500,
            content=response.model_dump(),
        )


def _get_status_title(status_code: int) -> str:
    """Get a human-readable title for an HTTP status code."""
    titles: dict[int, str] = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        409: "Conflict",
        422: "Unprocessable Entity",
        429: "Too Many Requests",
        500: "Internal Server Error",
    }
    return titles.get(status_code, "HTTP Error")
