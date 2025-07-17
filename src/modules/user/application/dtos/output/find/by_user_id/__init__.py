# /src/modules/user/application/dtos/output/find/by_user_id/__init__.py

# PY
from dataclasses import dataclass, fields
from typing import Any


@dataclass(frozen=True)
class FindUserByUserIdOutput:
    """
    Class representing the output DTO for the FindUserByUserId use case.

    Represents the response structure returned when retrieving a user
    by their unique identifier.

    Class Args:
        user_id (str): The unique identifier of the user.
        name (str): The user's full name.
        email (str): The user's email address.
        status (str): The user's current status (e.g., 'active').
    """
    user_id: str
    name: str
    email: str
    status: str

    @classmethod
    def from_entity(cls, entity: Any) -> "FindUserByUserIdOutput":
        """
        Class method that creates an instance of FindUserByUserIdOutput
            from a domain entity.

        Automatically maps matching fields from the entity to the DTO
        based on attribute names.

        Args:
            entity (Any): The user domain entity or model to be converted.

        Returns:
            FindUserByUserIdOutput: A DTO populated with data from the entity.
        """
        field_names = {f.name for f in fields(cls)}

        data = {}
        for key in field_names:
            value = getattr(entity, key, None)
            # if key.endswith("id") and value is not None:
            #     log.debug(f"Converting {key} to string: {value}")
            data[key] = value

        return cls(**data)
