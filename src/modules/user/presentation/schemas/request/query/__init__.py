# /src/modules/user/presentation/schemas/request/query/__init__.py

# Domain
from src.domain.dtos.base import BaseDTO


class FindUserByUserIdQuerySchema(BaseDTO):
    """
    Class responsible for the Data Transfer Object
        (DTO) for retrieving a user by user_id.

    This class validates and structures query parameters
        used to fetch a specific user,
        ensuring that the required identifier
        is provided for user-related lookup operations.

    Validation mode: 'query'.
    """

    __validation_mode__ = "query"

    user_id: str | None = None
