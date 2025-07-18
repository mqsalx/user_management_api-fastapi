# /src/data/models/permission/__init__.py

# flake8: noqa: E501

# PY
import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import Session, relationship

# core
from src.core.configurations import (
    EnvConfig,
    DatabaseConfig
)

# data
from src.data.models.role_permission import role_permission

# Utils
from src.utils.generator import GenUtil
from src.utils.logger import log


Base = DatabaseConfig.base()


class PermissionModel(Base):
    """
    Class responsible for defining the database model for permissions.

    This model represents the `permissions` table and manages permission-related
    relationships and data operations.

    Class Args:
        None
    """

    __tablename__ = "permissions"

    _unique_id = GenUtil.generate_unique_id()

    permission_id = Column(
        String,
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    roles = relationship(
        "RoleModel", secondary=role_permission, back_populates="permissions"
    )

    @classmethod
    def create_permissions(cls) -> None:
        """
        Class method responsible for creating new permissions.

        This method retrieves permissions from the environment configuration and
        inserts them into the database if they do not already exist.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: If an error occurs during database operations.
        """

        db: Session = next(DatabaseConfig.get_db())

        __permissions = EnvConfig().api_role_permissions

        try:

            if not __permissions:
                return

            existing_permissions = {
                permission.permission_id for permission in db.query(cls).all()
            }

            new_permissions = [
                cls(
                    permission_id=permission
                )
                for permission in __permissions
                if permission not in existing_permissions
            ]

            if new_permissions:
                db.add_all(new_permissions)
                db.commit()
            else:
                return

        except Exception as error:
            db.rollback()
            log.error(f"Error in create_permissions: {error}")

        finally:
            db.close()
