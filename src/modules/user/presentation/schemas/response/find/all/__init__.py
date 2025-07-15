# /src/modules/user/presentation/schemas/response/find/all/__init__.py

from typing import List

from pydantic import BaseModel

from src.modules.user.application.dtos.output.find.by_user_id import (
    FindUserByUserIdOutput,
)
from src.modules.user.presentation.schemas.response.find.by_user_id import (
    FindUserByUserIdResponse,
)


class FindAllUsersResponse(BaseModel):
    """ """

    pagination: "PaginatedResponse"
    items: List[FindUserByUserIdResponse]

    @classmethod
    def format(
        cls,
        output: list[FindUserByUserIdOutput],
        pagination: "PaginatedResponse",
    ) -> "FindAllUsersResponse":
        """ """
        instance = cls(
            items=[
                FindUserByUserIdResponse.format(output=user) for user in output
            ],
            pagination=pagination,
        )
        
        return instance.model_dump()


class PaginatedResponse(BaseModel):
    """ """

    page: int
    limit: int
    actual_limit: int
    max_limit: int
    total_items: int
    total_pages: int
    order: str
