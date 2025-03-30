from nexios.middlewares.base import BaseMiddleware
from nexios.http import Request, Response
from typing_extensions import Annotated, Doc
import typing
from typing import Any
from nexios.config import get_config


class CommonMiddleware(BaseMiddleware):
    """
    Middleware for applying common security and response headers.

    This middleware enhances security by enforcing strict HTTP headers,
    including `X-Frame-Options`, `Strict-Transport-Security`, `Content-Security-Policy`,
    and other best practices.

    It prevents caching of sensitive data, ensures proper content handling,
    and restricts browser behaviors that could lead to security vulnerabilities.
    """

    async def process_request(
        self,
        request: Annotated[
            Request,
            Doc("The incoming HTTP request."),
        ],
        response: Annotated[
            Response,
            Doc("The HTTP response object that will be returned."),
        ],
        call_next: typing.Callable[..., typing.Awaitable[Any]],
    ) -> None:
        """
        Process the incoming request before it reaches the route handler.

        This method can be extended for request validation, logging,
        or additional security checks.

        Args:
            request (Request): The incoming HTTP request.
            response (Response): The response object (not modified here).

        Returns:
            None
        """
        await call_next()

    async def process_response(
        self,
        request: Annotated[
            Request,
            Doc("The HTTP request associated with the response."),
        ],
        response: Annotated[
            Response,
            Doc("The response object modified before being sent."),
        ],
    ) -> None:
        """
        Process the outgoing response and add security headers.

        This method applies security and cache-control headers based on
        the application's configuration.

        Args:
            request (Request): The HTTP request object.
            response (Response): The response object to be modified.

        Returns:
            None
        """
        self.config = get_config()
        response.header("X-Frame-Options", "DENY")
        response.header("X-XSS-Protection", "1; mode=block")
        response.header("X-Content-Type-Options", "nosniff")
        response.header(
            "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
        )
        response.header(
            "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
        )
        response.header("Pragma", "no-cache")

        if self.config.content_security_policy:
            response.header(
                "Content-Security-Policy", self.config.content_security_policy
            )

        if self.config.permissions_policy:
            response.header("Permissions-Policy", self.config.permissions_policy)

        if self.config.referrer_policy:
            response.header("Referrer-Policy", self.config.referrer_policy)

        if self.config.feature_policy:
            response.header("Feature-Policy", self.config.feature_policy)

        if request.user_agent:
            response.header("X-User-Agent", request.user_agent)
