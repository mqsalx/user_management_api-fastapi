from dataclasses import dataclass

from src.shared.domain.entities.base import BaseEntity


@dataclass
class UserEntity(BaseEntity):
    """
    Class representing a domain entity for a user within the system.

    This entity is used throughout the domain and application layers
    to encapsulate user-related data and behavior.

    Attributes:
        user_id (str | None): The unique identifier of the user.
        name (str | None): The full name of the user.
        email (str | None): The user's email address.
        password (str | None): The hashed password of the user.
        status (str | None): The status of the user (e.g., active, inactive).
        role_id (str | None): The ID of the role associated with the user.
    """
    user_id: str | None = None
    name: str | None = None
    email: str | None = None
    password: str | None = None
    status: str | None = None
    role_id: str | None = None

    def __post_init__(self) -> None:
        """
        Post-initialization method to synchronize user_id and entity_id.

        Ensures consistency between the user_id and the
            base entity's entity_id.
        If user_id is provided, it will override the entity_id.
        If user_id is not provided, the generated entity_id
            will be used as the user_id.
        """

        if self.user_id:
            self.entity_id = self.user_id
        else:
            self.user_id = self.entity_id
