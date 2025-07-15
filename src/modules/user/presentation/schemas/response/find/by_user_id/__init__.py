# /src/modules/user/presentation/schemas/response/find/by_user_id/__init__.py

from pydantic import BaseModel

from src.modules.user.application.dtos.output.find.by_user_id import (
    FindUserByUserIdOutput,
)


class FindUserByUserIdResponse(BaseModel):
    """ """

    name: str
    email: str
    status: str

    @classmethod
    def format(
        cls, output: FindUserByUserIdOutput
    ) -> "FindUserByUserIdResponse":
        instance = cls(
            name=output.name,
            email=output.email,
            status=output.status,
        )

        return instance.model_dump()
