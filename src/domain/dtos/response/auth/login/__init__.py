# /src/domain/dtos/response/auth/login/__init__.py

# flake8: noqa: E501

from pydantic import RootModel


class LoginResponseDTO(RootModel):
    """
    Data Transfer Object (DTO) for user login responses.

    This class structures the login response, returning login-related data.

    Class Args:
        None
    """

    root: dict[str, str]
