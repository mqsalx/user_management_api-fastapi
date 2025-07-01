# /src/domain/usecases/auth/validate/__init__.py

# flake8: noqa: E501

from typing import Any, Dict

from fastapi import Request

# Core
from src.core.exceptions import (
    BaseHTTPException,
    InvalidTokenException,
    InvalidTokenOrIncorrectPayloadException
)

# Utils
from src.utils import (
    AuthUtil,
    log
)


class ValidateUseCase:
    """
    Class responsible for handling the authentication use case.

    This class manages user authentication by verifying credentials
    and generating JWT tokens.
    """

    def __call__(self, request: Request) -> Dict[str, Any]:
        """
        Public method responsible for authenticating a user and returning a JWT token.

        This method verifies the user's email and password. If authentication is successful,
        it generates a JWT token containing user details.

        Args:
            body (AuthenticationRequestDTO): The DTO containing the user's email and password.

        Returns:
            Dict[str, str]: A dictionary containing the access token and token type.

        Raises:
            InvalidCredentialsException: If the email or password is incorrect.
            BaseException: If an unexpected error occurs during authentication.
        """

        try:

            access_token = getattr(request.state, "access_token", None)

            if not access_token:
                raise InvalidTokenException("Token missing or invalid!")

            payload: Any = AuthUtil.verify_token(access_token)

            if not payload:

                raise InvalidTokenOrIncorrectPayloadException("Invalid token or invalid payload!")

            return {
                    "user_id": dict(payload).get("user_id"),
                    "role": dict(payload).get("role")
                }

        except (
            Exception,
            BaseHTTPException
        ) as error:
            log.error(f"Error authenticating user: {error}")
            raise
