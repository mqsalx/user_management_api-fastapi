# /src/api/schemas/user/request/body/__init__.py

# PY
from pydantic.dataclasses import dataclass


@dataclass
class CreateUserReq:
    """
    Class representing the request body schema for creating a new user.

    This data class defines the required fields to register a new user
    in the system. It is used in POST endpoints.

    Class Args:
        name (str): The full name of the user.
        email (str): The user's email address.
        password (str): The user's plain-text password (to be hashed).
        status (str): The initial status of the user (e.g., 'active').
    """
    name: str
    email: str
    password: str
    status: str


@dataclass
class UpdateUserReq:
    """
    Class representing the request body schema for updating an existing user.

    This data class defines optional fields that can be updated for a user.
    It is used in PUT or PATCH endpoints. Only fields that are not `None`
    will be considered for update.

    Class Args:
        user_id (str): The unique identifier of the user to update.
        name (str | None): The new name of the user.
        email (str | None): The new email address of the user.
        password (str | None): The new password (plain-text).
        role_id (str | None): The new role identifier.
        status (str | None): The new status of the user.
    """
    user_id: str
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role_id: str | None = None
    status: str | None = None
