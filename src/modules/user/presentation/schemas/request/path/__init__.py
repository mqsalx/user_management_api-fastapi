# /src/api/schemas/user/request/path/__init__.py

# PY
from fastapi import Path
from pydantic.dataclasses import dataclass


@dataclass
class FindUserByUserIdReq:
    """
    Class representing the request path parameter schema
        for finding a user by ID.

    This schema is used in GET endpoints that require a user ID in the path.

    Class Args:
        user_id (str): The ID of the user to be found.
    """
    user_id: str = Path(..., description="The ID of the user to be found.")


@dataclass
class RemoveUserReq:
    """
    Class representing the request path parameter schema
        for removing a user by ID.

    This schema is used in DELETE endpoints that target a specific user.

    Class Args:
        user_id (str): The ID of the user to be removed.
    """
    user_id: str = Path(..., description="The ID of the user to be removed.")
