# /src/infrastructure/models/user_role_model.py

from sqlalchemy import Column, String
from sqlalchemy.orm import Session, relationship

from src.core.configurations.env_configuration import EnvConfiguration
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)
from src.infrastructure.models.permission_model import PermissionModel
from src.infrastructure.models.role_permission_model import role_permission
from src.utils.any_utils import AnyUtils
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()

Base = DatabaseConfiguration.base()


class RoleModel(Base):

    __tablename__ = "roles"

    _unique_id = AnyUtils.generate_unique_id()

    id = Column(String, nullable=False)

    role_id = Column(String, primary_key=True, nullable=False)

    permissions = relationship(
        PermissionModel, secondary=role_permission, back_populates="roles"
    )

    @classmethod
    def create_roles(cls) -> None:
        """

        """
        db: Session = next(DatabaseConfiguration.get_db())
        __roles = EnvConfiguration().api_user_roles

        try:

            if not __roles:
                return

            existing_roles = {role.role_id for role in db.query(cls).all()}

            new_roles = [
                cls(id=AnyUtils.generate_unique_id(), role_id=role)
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
        """ """
        db: Session = next(DatabaseConfiguration.get_db())
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
