# /src/api/schemas/base/request/query/__init__.py

# PY
from fastapi import Query
from pydantic.dataclasses import dataclass


@dataclass
class BaseQueryReq:
    """
    Base query parameters for paginated and ordered API requests.

    This class defines common query parameters used
        in list endpoints to support pagination and sorting.

    It is intended to be extended or used directly
    in FastAPI route dependencies via `Depends()`.

    Class Args:
        page (int): Page number for pagination (default: 1).
        limit (int): Maximum number of results to return per page (default: 1).
        order (str): Result sorting order,
            either 'asc' or 'desc' (default: 'asc').
    """

    page: int = Query(default=1, description="Page number for pagination.")
    limit: int = Query(default=1, description="Number of results to return.")
    order: str = Query(
        default="asc",
        description="Order of the results, either 'asc' or 'desc'.",
    )
