# /src/infrastructure/models/user_role_model.py


from sqlalchemy import Column, String
from sqlalchemy.orm import Session, relationship

from src.core.configurations.env_configuration import EnvConfiguration
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)
from src.infrastructure.models.role_permission_model import role_permission
from src.utils.any_utils import AnyUtils
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()

Base = DatabaseConfiguration.base()


class PermissionModel(Base):

    __tablename__ = "permissions"

    _unique_id = AnyUtils.generate_unique_id()

    id = Column(String, nullable=False)
    permission_id = Column(String, primary_key=True, nullable=False)

    roles = relationship(
        "RoleModel", secondary=role_permission, back_populates="permissions"
    )

    @classmethod
    def create_permissions(cls) -> None:
        """ """
        db: Session = next(DatabaseConfiguration.get_db())

        __permissions = EnvConfiguration().api_role_permissions

        try:

            if not __permissions:
                return

            existing_permissions = {
                permission.permission_id for permission in db.query(cls).all()
            }

            new_permissions = [
                cls(id=AnyUtils.generate_unique_id(), permission_id=permission)
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
