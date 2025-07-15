# /src/modules/user/application/commands/create/__init__.py

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserInput:
    """
    """
    name: str
    email: str
    password: str
    status: str
