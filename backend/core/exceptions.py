"""
Custom exception classes and RFC 7807 error response handling.
"""

from typing import Any, Optional

from fastapi import status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """RFC 7807 Problem Details response format."""

    type: str
    title: str
    status: int
    detail: str
    instance: Optional[str] = None


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        title: str,
        detail: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        exception_type: str = "about:blank",
        instance: Optional[str] = None,
    ):
        self.title = title
        self.detail = detail
        self.status_code = status_code
        self.exception_type = exception_type
        self.instance = instance
        super().__init__(detail)

    def to_response(self) -> dict[str, Any]:
        """Convert exception to RFC 7807 response format."""
        return {
            "type": self.exception_type,
            "title": self.title,
            "status": self.status_code,
            "detail": self.detail,
            "instance": self.instance,
        }


class ValidationException(AppException):
    """Raised when request validation fails."""

    def __init__(self, detail: str, instance: Optional[str] = None):
        super().__init__(
            title="Validation Error",
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            exception_type="https://fastapi.tiangolo.com/errors/validation-error",
            instance=instance,
        )


class NotFoundException(AppException):
    """Raised when a resource is not found."""

    def __init__(self, detail: str = "Resource not found", instance: Optional[str] = None):
        super().__init__(
            title="Not Found",
            detail=detail,
            status_code=status.HTTP_404_NOT_FOUND,
            exception_type="https://httpwg.org/specs/rfc7231.html#status.404",
            instance=instance,
        )


class UnauthorizedException(AppException):
    """Raised when authentication fails."""

    def __init__(self, detail: str = "Unauthorized", instance: Optional[str] = None):
        super().__init__(
            title="Unauthorized",
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            exception_type="https://httpwg.org/specs/rfc7235.html#status.401",
            instance=instance,
        )


class ForbiddenException(AppException):
    """Raised when user lacks required permissions."""

    def __init__(self, detail: str = "Forbidden", instance: Optional[str] = None):
        super().__init__(
            title="Forbidden",
            detail=detail,
            status_code=status.HTTP_403_FORBIDDEN,
            exception_type="https://httpwg.org/specs/rfc7231.html#status.403",
            instance=instance,
        )


class ConflictException(AppException):
    """Raised when request conflicts with existing resource."""

    def __init__(self, detail: str = "Conflict", instance: Optional[str] = None):
        super().__init__(
            title="Conflict",
            detail=detail,
            status_code=status.HTTP_409_CONFLICT,
            exception_type="https://httpwg.org/specs/rfc7231.html#status.409",
            instance=instance,
        )


class RateLimitException(AppException):
    """Raised when rate limit is exceeded."""

    def __init__(self, detail: str = "Too many requests", instance: Optional[str] = None):
        super().__init__(
            title="Too Many Requests",
            detail=detail,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            exception_type="https://httpwg.org/specs/rfc6585.html#status.429",
            instance=instance,
        )
