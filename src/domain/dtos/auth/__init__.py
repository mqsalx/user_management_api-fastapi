# /src/domain/dtos/auth/__init__.py

# flake8: noqa: E501

from pydantic import BaseModel, RootModel


class AuthRequestDTO(BaseModel):
    """
    Class responsible for the Data Transfer Object (DTO) for user login requests.

    This class is used to validate and structure login request payloads.

    Class Args:
        None
    """

    email: str
    password: str


class AuthResponseDTO(RootModel):
    """
    Data Transfer Object (DTO) for user login responses.

    This class structures the login response, returning authentication-related data.

    Class Args:
        None
    """

    root: dict[str, str]
