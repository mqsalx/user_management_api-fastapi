# /src/modules/user/application/commands/remove/__init__.py

from dataclasses import dataclass


@dataclass(frozen=True)
class RemoveUserInput:
    """
    """
    user_id: str
