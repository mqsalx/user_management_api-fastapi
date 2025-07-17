# /src/modules/user/application/dtos/input/create/__init__.py

# PY
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserInput:
    """
    Class representing the input DTO (Data Transfer Object)
        for the CreateUser use case.

    This class encapsulates the data required to create a new user,
        and is used by the application layer to pass validated input
        from the controller or handler to the use case logic.

    Class Args:
        name (str): The full name of the user.
        email (str): The user's email address.
        password (str): The user's plain-text password
            (to be hashed internally).
        status (str): The initial status of the user (e.g., 'active').
    """
    name: str
    email: str
    password: str
    status: str
