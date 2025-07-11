# /src/modules/user/application/commands/create/__init__.py

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserCommand:
    """
    Command object representing the data required to create a new user.

    This command is used in the application layer
        as part of the command pattern.
    It encapsulates all necessary attributes needed to
        perform the user creation
        use case, ensuring immutability with `frozen=True`.
    """
    name: str
    email: str
    password: str
    status: str
