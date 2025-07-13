from dataclasses import dataclass

from src.shared.domain.entities.base import BaseEntity


@dataclass
class UserEntity(BaseEntity):
    """
    Domain entity representing a user within the system.
    """
    user_id: str | None = None
    name: str | None = None
    email: str | None = None
    password: str | None = None
    status: str | None = None
    role_id: str | None = None

    def __post_init__(self) -> None:
        """
        Post-initialization to ensure user_id is set correctly.
        If user_id is provided, it will be used as entity_id.
        If user_id is not provided, entity_id will be used as user_id.
        """
        if self.user_id:
            self.entity_id = self.user_id
        else:
            self.user_id = self.entity_id
