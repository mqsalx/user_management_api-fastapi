# /src/modules/user/application/queries/find_user_by_id/__init__.py

from dataclasses import dataclass


@dataclass(frozen=True)
class FindUserByUserIdQuery:
    """
    Query object used to retrieve a user by their unique identifier.

    This query is used in the application layer to encapsulate
    the input required for the user retrieval use case.
    """
    user_id: str
