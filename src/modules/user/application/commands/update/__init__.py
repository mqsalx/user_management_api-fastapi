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
    name: str | None = None
    email: str | None = None
    status: str | None = None
    password: str | None = None
    role_id: str | None = None
