# /src/modules/user/domain/entities/__init__.py

# PY
from dataclasses import dataclass
from datetime import datetime

# Shared
from src.shared.domain.entities.base import BaseEntity


@dataclass
class UserEntity(BaseEntity):
    """
    """

    name: str
    email: str
    password: str
    status: str

    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        status: str,
        user_id: str | None = None,
        role_id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        super().__init__(
            entity_id=user_id, created_at=created_at, updated_at=updated_at
        )
        self.name = name
        self.email = email
        self.password = password
        self.status = status
        self.user_id: str | None = user_id
        self.role_id: str | None = role_id

    @staticmethod
    def create(
        name: str, email: str, password_hash: str, status: str
    ) -> "UserEntity":
        return UserEntity(
            name=name, email=email, password=password_hash, status=status
        )
