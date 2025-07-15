# /src/modules/user/application/queries/find_user_by_id/__init__.py

from dataclasses import dataclass


@dataclass(frozen=True)
class FindUserByUserIdInput:
    """
    """
    user_id: str
