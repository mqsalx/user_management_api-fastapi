# /src/modules/user/presentation/schemas/response/create/__init__.py

# Shared
from src.shared.presentation.schemas.base import BaseSchema

from src.modules.user.application.dtos.output.create import (
    CreateUserOutput
)


class CreateUserResponse(BaseSchema):
    """
    """

    user_id: str
    name: str
    email: str
    status: str
    role_id: str

    @classmethod
    def format(
        cls, output: CreateUserOutput
    ) -> "CreateUserResponse":
        instance = cls(
            user_id=output.user_id,
            name=output.name,
            email=output.email,
            status=output.status,
            role_id=output.role_id,
        )

        return instance.model_dump()
