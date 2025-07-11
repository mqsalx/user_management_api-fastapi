# /src/modules/user/application/commands/remove/__init__.py

from dataclasses import dataclass


@dataclass(frozen=True)
class RemoveUserCommand:
    """
    Command object representing the intent to remove a user.

    This command is used in the application layer to encapsulate
    the data required to execute the user removal use case.
    """
    user_id: str
