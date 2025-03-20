# /src/infrastructure/models/user_role_model.py


from sqlalchemy import Column, ForeignKey, String, Table

from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)

Base = DatabaseConfiguration.base()


"""
Table responsible for defining the many-to-many relationship between roles and permissions.

This table acts as a bridge between the `roles` and `permissions` tables,
allowing multiple roles to have multiple permissions.
"""

role_permission = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", String, ForeignKey("roles.role_id"), primary_key=True),
    Column(
        "permission_id",
        String,
        ForeignKey("permissions.permission_id"),
        primary_key=True,
    ),
)
