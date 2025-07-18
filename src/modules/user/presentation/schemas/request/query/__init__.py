# /src/api/schemas/user/request/query/__init__.py

# PY
from pydantic.dataclasses import dataclass

# Api
from src.api.schemas.base.request.query import BaseQueryReq


@dataclass
class FindAllUsersReq(BaseQueryReq):
    """
    Class representing the request Query parameter schema
        for retrieving a paginated list of users.

    Inherits from `BaseQueryReq` and provides standard pagination and ordering
    capabilities for list endpoints.

    This schema is typically used in GET endpoints to filter
        and paginate user records.
    """
    pass
