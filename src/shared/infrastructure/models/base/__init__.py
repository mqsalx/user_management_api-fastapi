# /src/shared/infrastructure/models/base/__init__.py

# PY
from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

# Core
from src.core.configurations import db_config, env_config

Base = db_config.base()


class BaseModel(Base):
    """
    Base abstract model for all ORM entities in the application.

    This class dynamically defines the following for its subclasses:
    - A table name based on the class name.
    - A UUID primary key with a dynamic column name based on the model name (e.g., 'user_id').
    - Common timestamp fields: created_at and updated_at.

    Intended to be inherited by concrete SQLAlchemy models.
    """

    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> Any:
        """
        Generates the table name dynamically from the class name by:
        - Removing the 'Model' suffix.
        - Converting to lowercase.
        - Appending 's' (simple pluralization).

        Example:
            UserModel → 'users'
            RoleModel → 'roles'

        Returns:
            str: The table name to use for the SQLAlchemy model.
        """
        return cls.__name__.replace("Model", "").lower() + "s"

    @declared_attr
    def __mapper_args__(cls) -> Any:
        """
        Optional SQLAlchemy mapper configuration.

        Enables eager loading of default values
            (e.g., UUID, timestamps) after inserts.

        Returns:
            dict: Mapper configuration dictionary.
        """
        return {"eager_defaults": True}

    @declared_attr
    def __table_args__(cls) -> Any:
        """
        Provides table-level arguments for SQLAlchemy models.

        Sets the schema dynamically based on the class attribute `__schema__`,
            or defaults to the configured schema from the environment.
            Also sets `extend_existing=True` to allow
            redefinition during metadata reflection.

        Returns:
            dict: A dictionary of SQLAlchemy table arguments.
        """
        return {
            "schema": getattr(
                cls,
                "__schema__",
                env_config.database_schema
            ),
            "extend_existing": True,
        }

    @declared_attr
    def is_active(cls) -> Mapped[bool]:
        """
        Declares a boolean column to indicate whether the record is active.

        This is useful for soft-deletion or status-based filtering.

        Returns:
            Mapped[bool]: A boolean column with default True.
        """
        return mapped_column(Boolean, default=True, nullable=False)

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        """
        Declares a timestamp for when the row was created.

        Uses PostgreSQL `now()` as the default value.

        Returns:
            sqlalchemy.orm.mapped_column: The created_at timestamp column.
        """
        return mapped_column(
            DateTime,
            default=func.now(),
            nullable=False
        )

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        """
        Declares a timestamp for when the row was last updated.

        Automatically updated with the current timestamp on modification.

        Returns:
            sqlalchemy.orm.mapped_column: The updated_at timestamp column.
        """
        return mapped_column(
            DateTime,
            default=func.now(),
            onupdate=func.now(),
            nullable=True
        )

    @classmethod
    def id_name(cls) -> str:
        """
        Returns the name of the primary key column dynamically.

        Useful for generic repositories that need to filter by primary key
        without knowing its name ahead of time.

        Returns:
            str: Name of the primary key column (e.g., 'user_id')
        """
        for column in cls.__table__.columns:
            if column.primary_key:
                return column.name
        raise RuntimeError(f"No primary key defined for model {cls.__name__}")