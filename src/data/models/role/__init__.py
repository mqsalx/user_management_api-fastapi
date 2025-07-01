# /src/data/models/role/__init__.py

# flake8: noqa: E501

# PY
import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import Session, relationship

# Core
from src.core.configurations import (
    EnvConfig,
    DatabaseConfig
)

# Data
from src.data.models import PermissionModel
from src.data.models.role_permission import role_permission

# Utils
from src.utils.generator import GenUtil
from src.utils.logger import log


Base = DatabaseConfig.base()


class RoleModel(Base):
    """
    Class responsible for defining the database model for roles.

    This model represents the `roles` table and manages role-related relationships
    and data operations.

    Table Name:
        roles

    Class Args:
        None
    """

    __tablename__ = "roles"

    _unique_id = GenUtil.generate_unique_id()

    role_id = Column(
        String,
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    permissions = relationship(
        PermissionModel, secondary=role_permission, back_populates="roles"
    )

    @classmethod
    def create_roles(cls) -> None:
        """
        Class method responsible for creating new roles.

        This method retrieves roles from the environment configuration and inserts
        them into the database if they do not already exist.

        Returns:
            None

        Raises:
            Exception: If an error occurs during database operations.
        """

        db: Session = next(DatabaseConfig.get_db())
        __roles = EnvConfig().api_user_roles

        try:

            if not __roles:
                return

            existing_roles = {role.role_id for role in db.query(cls).all()}

            new_roles = [
                cls(role_id=role)
                for role in __roles
                if role not in existing_roles
            ]

            if new_roles:
                db.add_all(new_roles)
                db.commit()
            else:
                return

        except Exception as error:
            db.rollback()
            log.error(f"Error in the process of creating roles: {error}")

        finally:
            db.close()

    @classmethod
    def assign_permissions_to_administrator(cls):
        """
        Class method responsible for assigning all permissions to the 'Administrator' role.

        This method retrieves the 'Administrator' role from the database and assigns
        all available permissions to it.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: If an unexpected error occurs while assigning permissions.
        """

        db: Session = next(DatabaseConfig.get_db())
        try:
            administrator_role = (
                db.query(cls).filter_by(role_id="administrator").first()
            )
            if not administrator_role:
                log.info("Role: 'administrator' not found in the database.")
                return

            all_permissions = db.query(PermissionModel).all()

            if not all_permissions:

                log.info("No permissions found in the database.")
                return

            administrator_role.permissions = all_permissions

            db.commit()
            log.info(
                f"Linked {len(all_permissions)} permissions to the 'Administrator' role."
            )

        except Exception as error:
            db.rollback()
            log.error(
                f"Error linking permissions to the 'Administrator' role: {error}"
            )
