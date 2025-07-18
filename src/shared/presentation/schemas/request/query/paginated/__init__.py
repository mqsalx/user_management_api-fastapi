# /src/shared/presentation/schemas/request/query/paginated/__init__.py


from src.shared.presentation.schemas.request.base import BaseRequest


class PaginatedQuerySchema(BaseRequest):
    """
    """
    __action_type__ = "query"

    page: int = 1
    limit: int = 1
    order: str = "asc"
