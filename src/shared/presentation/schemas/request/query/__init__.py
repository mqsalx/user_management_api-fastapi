# /src/shared/presentation/schemas/request/query/__init__.py

from fastapi import Query
from pydantic.dataclasses import dataclass


@dataclass
class BaseQueryReq:
    page: int = Query(default=1, description="Page number for pagination.")
    limit: int = Query(default=1, description="Number of results to return.")
    order: str = Query(
        default="asc", description="Order of the results, either 'asc' or 'desc'."
    )
