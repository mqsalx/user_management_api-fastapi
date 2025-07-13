# /src/modules/user/application/queries/find_all_users/__init__.py

# PY
from dataclasses import dataclass


@dataclass(frozen=True)
class FindAllUsersQuery:
    """
    """
    page: int
    limit: int
    order: str
