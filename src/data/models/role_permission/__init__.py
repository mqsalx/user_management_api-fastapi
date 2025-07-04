# /src/data/models/role_permission/__init__.py

# flake8: noqa: E501

# PY
from sqlalchemy import Column, ForeignKey, String, Table

# Core
from src.core.configurations import db_config

Base = db_config.base()


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
