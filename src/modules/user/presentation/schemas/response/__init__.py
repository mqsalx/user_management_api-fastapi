# /src/domain/dtos/response/user/__init__.py

# Shared
from src.shared.presentation.schemas.base import BaseSchema


class UserResponseSchema(BaseSchema):
    """
    """

    user_id: str
    name: str
    email: str
    status: str
