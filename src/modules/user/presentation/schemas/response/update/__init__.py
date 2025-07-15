# /src/modules/user/presentation/schemas/response/find/by_user_id/__init__.py

from pydantic import BaseModel

from src.modules.user.application.dtos import (
    UpdateUserOutput,
)


class UpdateUserResponse(BaseModel):
    """ """

    user_id: str
    name: str
    email: str
    status: str
    role_id: str

    @classmethod
    def format(
        cls, output: UpdateUserOutput
    ) -> "UpdateUserResponse":
        instancce =  cls(
            name=output.name,
            email=output.email,
            status=output.status,
            user_id=output.user_id,
            role_id=output.role_id,
        )

        return instancce.model_dump()
