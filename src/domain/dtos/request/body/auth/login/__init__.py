# /src/domain/dtos/request/body/auth/login/__init__.py

# flake8: noqa: E501

from src.domain.dtos.base import BaseDTO


class LoginRequestDTO(BaseDTO):
    """
    Class responsible for the Data Transfer Object (DTO) for user login requests.

    This class is used to validate and structure login request payloads.

    Class Args:
        None
    """

    email: str
    password: str
