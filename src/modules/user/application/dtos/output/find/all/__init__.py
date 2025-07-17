# /src/modules/user/application/dtos/output/find/all/__init__.py

# PY
from dataclasses import dataclass

# Modules
from src.modules.user.application.dtos.output.find.by_user_id import (
    FindUserByUserIdOutput,
)
from src.modules.user.domain.entities import UserEntity


@dataclass(frozen=True)
class FindAllUsersOutput:
    """
    Class representing the output DTO for the FindAllUsers use case.

    Represents the result of a paginated user listing, including user data
    and associated pagination metadata.

    Class Args:
        pagination (PaginationOutput): Metadata describing
            pagination state and limits.
        data (list[FindUserByUserIdOutput]): A list of users returned
            in the current page.
    """
    pagination: "PaginationOutput"
    data: list[FindUserByUserIdOutput]

    @classmethod
    def format(
        cls, entities: list[UserEntity], pagination: "PaginationOutput"
    ) -> "FindAllUsersOutput":
        """
        Converts a list of UserEntity instances into a FindAllUsersOutput DTO.

        Args:
            entities (list[UserEntity]): List of user entities to
                include in the response.
            pagination (PaginationOutput): Pagination metadata
                for the current result set.

        Returns:
            FindAllUsersOutput: A DTO containing paginated user
                data and metadata.
        """
        return cls(
            data=[
                FindUserByUserIdOutput.from_entity(entity)
                for entity in entities
            ],
            pagination=pagination,
        )


@dataclass
class PaginationOutput:
    """
    Class representing pagination metadata in list responses.

    Used to describe the current page, limit, total items, and sorting
    behavior associated with a paginated result.

    Class Args:
        page (int): Current page number.
        limit (int): Requested limit (maximum number of items per page).
        actual_limit (int): Actual limit used in the query
            (may be adjusted internally).
        max_limit (int): Maximum allowable limit per page.
        total_items (int): Total number of items matching the query.
        total_pages (int): Total number of pages available
            based on total_items and limit.
        order (str): Sorting order used (e.g., 'asc' or 'desc').
    """
    page: int
    limit: int
    actual_limit: int
    max_limit: int
    total_items: int
    total_pages: int
    order: str
