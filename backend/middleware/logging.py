"""
Middleware for logging requests and responses.
"""

import logging
import time
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs all incoming requests and outgoing responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and log details.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware in chain

        Returns:
            Response from next middleware/endpoint
        """
        # Extract request information
        request_id = request.headers.get("x-request-id", "no-id")
        method = request.method
        path = request.url.path
        query_string = request.url.query

        # Log incoming request
        logger.info(
            f"[{request_id}] {method} {path} | Query: {query_string or 'none'}",
            extra={
                "request_id": request_id,
                "method": method,
                "path": path,
                "query": query_string,
            },
        )

        # Measure processing time
        start_time = time.time()

        try:
            response = await call_next(request)
        except Exception as exc:
            process_time = time.time() - start_time
            logger.error(
                f"[{request_id}] {method} {path} | Error after {process_time:.3f}s: {str(exc)}",
                extra={
                    "request_id": request_id,
                    "method": method,
                    "path": path,
                    "process_time": process_time,
                    "error": str(exc),
                },
                exc_info=True,
            )
            raise

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        status_code = response.status_code
        logger.info(
            f"[{request_id}] {method} {path} | Status: {status_code} | Time: {process_time:.3f}s",
            extra={
                "request_id": request_id,
                "method": method,
                "path": path,
                "status_code": status_code,
                "process_time": process_time,
            },
        )

        # Add response headers
        response.headers["x-process-time"] = str(process_time)
        response.headers["x-request-id"] = request_id

        return response
