# /src/modules/user/application/queries/find_user_by_id/__init__.py

from dataclasses import dataclass


@dataclass
class FindUserByIdQuery:
    user_id: str
