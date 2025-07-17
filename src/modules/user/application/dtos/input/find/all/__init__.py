# /src/modules/user/application/dtos/input/find/all/__init__.py

# PY
from dataclasses import dataclass


@dataclass(frozen=True)
class FindAllUsersInput:
    """
    Class representing the input DTO for the FindAllUsers use case.

    This class encapsulates pagination and sorting parameters
    provided by the client to retrieve a list of users.

    Class Args:
        page (int): The current page number to retrieve.
        limit (int): The maximum number of users to return per page.
        order (str): Sorting order for the results ('asc' or 'desc').
    """
    page: int
    limit: int
    order: str
