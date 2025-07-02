# /src/modules/auth/presentation/schemas/response/login/__init__.py

# flake8: noqa: E501

from pydantic import RootModel


class LoginResponse(RootModel):
    """
    Data Transfer Object (DTO) for user login responses.

    This class structures the login response, returning login-related data.

    Class Args:
        None
    """

    root: dict[str, str]
