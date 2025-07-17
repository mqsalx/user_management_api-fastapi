# /src/modules/user/application/dtos/input/find/by_user_id/__init__.py

# PY
from dataclasses import dataclass


@dataclass(frozen=True)
class FindUserByUserIdInput:
    """
    Class representing the input DTO for the FindUserByUserId use case.

    Represents the data required to retrieve a user by their unique identifier.

    Class Args:
        user_id (str): The unique identifier of the user to be retrieved.
    """
    user_id: str
