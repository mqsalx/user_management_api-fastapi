# /src/modules/user/application/dtos/output/find/all/__init__.py

from dataclasses import dataclass

from src.modules.user.application.dtos.output.find.by_user_id import (
    FindUserByUserIdOutput,
)
from src.modules.user.domain.entities import UserEntity


@dataclass(frozen=True)
class FindAllUsersOutput:
    """ """

    paginated: "PaginatedOutput"
    items: list[FindUserByUserIdOutput]

    @classmethod
    def format(
        cls, entities: list[UserEntity], pagination: "PaginatedOutput"
    ) -> "FindAllUsersOutput":
        """ """
        return cls(
            items=[
                FindUserByUserIdOutput.format(entity=entity)
                for entity in entities
            ],
            paginated=pagination,
        )


@dataclass
class PaginatedOutput:
    """ """

    page: int
    limit: int
    actual_limit: int
    max_limit: int
    total_items: int
    total_pages: int
    order: str
