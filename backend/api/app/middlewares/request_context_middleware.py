from __future__ import annotations

import uuid
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from api.app.shared.request_context import RequestContext, set_request_context
from api.app.shared.request_context import reset_request_context


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Initializes a RequestContext for every request.

    - Ensures a request/correlation id exists (from X-Request-Id or generated)
    - Stores it in request.state.correlation_id
    - Sets response header X-Request-Id
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable):
        correlation_id = (request.headers.get("X-Request-Id") or "").strip() or str(uuid.uuid4())
        request.state.correlation_id = correlation_id

        token = set_request_context(
            RequestContext(
                correlation_id=correlation_id,
                method=request.method,
                route=str(request.url.path),
            )
        )
        try:
            response = await call_next(request)
        finally:
            reset_request_context(token)

        response.headers.setdefault("X-Request-Id", correlation_id)
        return response
