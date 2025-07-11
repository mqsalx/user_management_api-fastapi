# /src/modules/user/application/commands/update/__init__.py

from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateUserCommand:
    """
    Command object representing the data required to update an existing user.

    This command is used in the application layer to encapsulate all fields
    necessary for performing a user update operation.
    """
    user_id: str
    name: str
    email: str
    status: str
