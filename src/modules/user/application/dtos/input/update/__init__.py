# /src/modules/user/application/dtos/input/update/__init__.py

from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateUserInput:
    """
    Class representing the input DTO for the UpdateUser use case.

    Represents the data required to update an existing user's information.
    Only non-null fields will be considered for the update.

    Class Args:
        user_id (str): The unique identifier of the user to be updated.
        name (str | None): The new name of the user (optional).
        email (str | None): The new email address of the user (optional).
        status (str | None): The updated status of the user
            (e.g., 'active') (optional).
        password (str | None): The new plain-text password (optional).
        role_id (str | None): The new role ID associated
            with the user (optional).
    """
    user_id: str
    name: str | None = None
    email: str | None = None
    status: str | None = None
    password: str | None = None
    role_id: str | None = None
