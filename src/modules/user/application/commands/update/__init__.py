# /src/modules/user/application/commands/update/__init__.py

from dataclasses import dataclass


@dataclass
class UpdateUserCommand:
    """
    """
    user_id: str
    name: str
    email: str
    status: str
