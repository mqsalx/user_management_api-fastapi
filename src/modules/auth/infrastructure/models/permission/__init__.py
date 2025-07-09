# /src/data/models/permission/__init__.py

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


class PermissionModel(BaseModel):
    """
    Class responsible for defining the database model for permissions.

    This model represents the `permissions` table
        and manages permission-related
        relationships and data operations.

    Class Args:
        None
    """


    permission_id: Column[str] = Column(
        String,
        primary_key=True,
        nullable=False,
        unique=True
    )

    roles = relationship(
        argument="RoleModel",
        secondary=role_permission,
        back_populates="permissions"
    )
