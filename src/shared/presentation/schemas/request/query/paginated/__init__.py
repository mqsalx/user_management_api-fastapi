# /src/shared/presentation/schemas/request/query/paginated/__init__.py


from src.shared.presentation.schemas.base import BaseSchema


class PaginatedQuerySchema(BaseSchema):
    """
    """
    __validation_mode__ = "query"

    page: int = 1
    limit: int = 1
    order: str = "asc"
