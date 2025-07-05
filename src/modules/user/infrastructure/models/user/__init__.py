# /src/modules/user/infrastructure/models/user/__init__.py

# PY
import uuid

from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

# Domain
from src.domain.enums import (
    UserRoleEnum,
    UserStatusEnum
)

# Shared
from src.shared.infrastructure.models.base import BaseModel


class UserModel(BaseModel):
    """
    Class responsible for defining the database model for users.

    This model represents the `users` table
        and manages user-related relationships
        and data operations.
    """
    user_id: Column[str] = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False
    )

    name: Column[str] = Column(
        String,
        nullable=False
    )

    email: Column[str] = Column(
        String,
        nullable=False,
        unique=True
    )

    password: Column[str] = Column(
        String,
        nullable=False
    )

    status: Column[str] = Column(
        Enum(
            UserStatusEnum,
            create_type=True
        ),
        default=UserStatusEnum.ACTIVE,
        nullable=False,
    )

    role_id: Column[str] = Column(
        String,
        ForeignKey("roles.role_id"),
        nullable=False,
        default=UserRoleEnum.DEFAULT.value,
    )

    # Relationships
    roles = relationship(
        argument="RoleModel",
        back_populates="users"
    )

    sessions = relationship(
        argument="SessionModel",
        back_populates="users",
        cascade="all, delete-orphan"
    )
