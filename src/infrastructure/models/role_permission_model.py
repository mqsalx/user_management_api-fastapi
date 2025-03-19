# /src/infrastructure/models/user_role_model.py


from sqlalchemy import Column, ForeignKey, String, Table

from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)

Base = DatabaseConfiguration.base()


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
