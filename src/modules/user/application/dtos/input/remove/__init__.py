# /src/modules/user/application/dtos/input/remove/__init__.py

# PY
from dataclasses import dataclass


@dataclass(frozen=True)
class RemoveUserInput:
    """
    Class representing the input DTO for the RemoveUser use case.

    This class encapsulates the data required to remove a user,
        and is used by the application layer to pass validated input
        from the controller or handler to the use case logic.

    Class Args:
        user_id (str): The unique identifier of the user to remove.
    """
    user_id: str
