# /src/infrastructure/models/user_model.py

from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.orm import Session, relationship

from src.core.enums.user_role_enum import UserRoleEnum
from src.core.configurations.env_configuration import EnvConfiguration
from src.core.enums.user_status_enum import UserStatusEnum
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)
from src.infrastructure.models.role_model import RoleModel
from src.utils.any_utils import AnyUtils, generate_password_hash
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()

Base = DatabaseConfiguration.base()


class UserModel(Base):
    """
    Class responsible for defining the database model for users.

    This model represents the `users` table and manages user-related relationships
    and data operations.

    Class Args:
        None
    """

    __api_name = EnvConfiguration().api_name
    __api_user_administrator = EnvConfiguration().api_user_administrator
    __api_password_administrator = (
        EnvConfiguration().api_password_administrator
    )

    __tablename__ = "users"

    _prefix_id = "U"
    _unique_id = AnyUtils.generate_unique_id()
    _custom_id = f"{_prefix_id}{_unique_id}"

    id = Column(String, nullable=False, default=_unique_id)
    user_id = Column(
        String, primary_key=True, nullable=False, default=_custom_id
    )
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    status = Column(
        Enum(UserStatusEnum), default=UserStatusEnum.ACTIVE, nullable=False
    )
    created_at = Column(
        String, nullable=False, default=AnyUtils.generate_formatted_datetime
    )
    updated_at = Column(
        String,
        nullable=False,
        default=AnyUtils.generate_formatted_datetime,
        onupdate=AnyUtils.generate_formatted_datetime,
    )

    role_id = Column(
        String,
        ForeignKey("roles.role_id"),
        nullable=False,
        default=UserRoleEnum.DEFAULT.value,
    )

    role = relationship(RoleModel, backref="users")

    @classmethod
    def create_administrator_user(cls) -> None:
        """
        Class method responsible for creating an administrator user.

        This method checks if an administrator user already exists in the database.
        If not, it creates a new administrator account with the `super_administrator` role.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: If an error occurs while creating the administrator user.
        """

        from src.infrastructure.models.role_model import RoleModel

        db: Session = next(DatabaseConfiguration.get_db())

        try:

            existing_user = (
                db.query(cls)
                .filter(cls.name == cls.__api_user_administrator)
                .first()
            )

            if not existing_user:

                super_administrator = (
                    db.query(RoleModel)
                    .filter(RoleModel.role_id == "super_administrator")
                    .first()
                )

                if not super_administrator:
                    log.error("Super Administrator role not found.")
                    return

                new_user = cls(
                    user_id=cls._custom_id,
                    name=cls.__api_user_administrator,
                    email=f"{cls.__api_user_administrator.lower()}@{cls.__api_name}.com",
                    password=generate_password_hash(
                        cls.__api_password_administrator
                    ),
                    role_id=super_administrator.role_id,
                    created_at=AnyUtils.generate_formatted_datetime(),
                )

                db.add(new_user)
                db.commit()

                log.info("User Administrator created successfully.")

            else:
                log.info(
                    "Administrator user already exists, ignoring creation."
                )

        except Exception as error:
            db.rollback()
            log.error(f"Error creating admin user: {error}")

        finally:
            db.close()
