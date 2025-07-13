# /src/modules/user/presentation/schemas/request/query/__init__.py

# Shared
from src.shared.presentation.schemas.base import BaseSchema
from src.shared.presentation.schemas.request.query.paginated import (
    PaginatedQuerySchema,
)


class FindAllUsersQuerySchema(PaginatedQuerySchema):
    """ """


class FindUserByUserIdQuerySchema(BaseSchema):
    """ """

    __validation_mode__ = "query"

    user_id: str
