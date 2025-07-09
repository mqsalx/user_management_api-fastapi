# /src/data/models/role/__init__.py

# PY
from sqlalchemy import (
    Column,
    String
)

from sqlalchemy.orm import relationship

from src.modules.auth.infrastructure.models.role_permission \
    import role_permission

# Shared
from shared.infrastructure.models.base import BaseModel


class RoleModel(BaseModel):
    """
    Class responsible for defining the database model for roles.

    This model represents the `roles` table
        and manages role-related relationships and data operations.

    Table Name:
        roles

    Class Args:
        None
    """


    role_id: Column[str] = Column(
        String,
        primary_key=True,
        nullable=False,
        unique=True
    )

    permissions = relationship(
        argument="PermissionModel",
        secondary=role_permission,
        back_populates="roles"
    )

    users = relationship(
        argument="UserModel",
        back_populates="roles"
    )
