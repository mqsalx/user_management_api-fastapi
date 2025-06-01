# /src/domain/dtos/request/query/user/__init__.py

# flake8: noqa: E501

# Domain
from src.domain.dtos.base import BaseDTO


class FindUserByUserIdQueryDTO(BaseDTO):
    """
    Class responsible for the Data Transfer Object (DTO) for retrieving a user by user_id.

    This class validates and structures query parameters used to fetch a specific user,
    ensuring that the required identifier is provided for user-related lookup operations.

    Validation mode: 'query'.

    Class Args:
        None.
    """

    __validation_mode__ = "query"

    user_id: str | None = None