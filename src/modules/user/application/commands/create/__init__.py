# /src/modules/user/application/commands/create/__init__.py

from dataclasses import dataclass


@dataclass
class CreateUserCommand:
    """
    """
    name: str
    email: str
    password: str
    status: str
