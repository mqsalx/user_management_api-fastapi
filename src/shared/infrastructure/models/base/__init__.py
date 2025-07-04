# /src/shared/infrastructure/models/base/__init__.py

import uuid

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column
from typing import Any, ClassVar
from src.core.configurations import db_config

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
    def __tablename__(cls) -> str:
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
    def __mapper_args__(cls):
        """
        Optional SQLAlchemy mapper configuration.

        Enables eager loading of default values (e.g., UUID, timestamps) after inserts.

        Returns:
            dict: Mapper configuration dictionary.
        """
        return {"eager_defaults": True}

    @declared_attr
    def id_column_name(cls) -> ClassVar[str]:
        return f"{cls.__name__.replace('Model', '').lower()}_id"

    @declared_attr
    def entity_id(cls) -> Mapped[str]:
        """
        Declares a UUID primary key column with a dynamic name.

        The column:
        - Uses PostgreSQL UUID type.
        - Automatically generates a UUID using `uuid.uuid4`.
        - Is non-nullable and acts as the primary key.

        Returns:
            sqlalchemy.orm.Column: The configured UUID primary key column.
        """
        return mapped_column(
            __name_pos=String,
            name=cls.id_column_name,
            primary_key=True,
            default=lambda: str(uuid.uuid4),
            nullable=False
        )

    @declared_attr
    def is_active(cls) -> Mapped[bool]:
        """

        """
        return mapped_column(
            Boolean,
            default=True,
            nullable=False
        )

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        """
        Declares a timestamp for when the row was created.

        Uses PostgreSQL `now()` as the default value.

        Returns:
            sqlalchemy.orm.mapped_column: The created_at timestamp column.
        """
        return mapped_column(
            DateTime(timezone=True),
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
            DateTime(timezone=True),
            onupdate=func.now(),
            nullable=True
        )
