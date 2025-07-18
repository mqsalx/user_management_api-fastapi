# /src/data/models/user/__init__.py

# flake8: noqa: E501

# PY
import uuid

from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.orm import Session, relationship

# Core
from src.core.configurations import (
    EnvConfig,
    DatabaseConfig
)

# Domain
from src.domain.enums import (
    UserRoleEnum,
    UserStatusEnum
)

# Data
from src.data.models.auth.session import SessionAuthModel
from src.data.models.role import RoleModel

# Utils
from src.utils.auth import AuthUtil
from src.utils.generator import GenUtil
from src.utils.logger import log



Base = DatabaseConfig.base()


class UserModel(Base):
    """
    Class responsible for defining the database model for users.

    This model represents the `users` table and manages user-related relationships
    and data operations.
    """

    __api_name = EnvConfig().api_name
    __api_user_administrator = EnvConfig().api_user_administrator
    __api_password_administrator = (
        EnvConfig().api_password_administrator
    )

    __tablename__ = "users"

    _prefix_id = "U"
    _unique_id = GenUtil.generate_unique_id()
    _custom_id = f"{_prefix_id}{_unique_id}"

    user_id = Column(
        String,
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    status = Column(
        Enum(UserStatusEnum),
        default=UserStatusEnum.ACTIVE,
        nullable=False
    )
    created_at = Column(
        String,
        nullable=False,
        default=GenUtil.generate_formatted_datetime
    )
    updated_at = Column(
        String,
        nullable=False,
        default=GenUtil.generate_formatted_datetime,
        onupdate=GenUtil.generate_formatted_datetime,
    )

    role_id = Column(
        String,
        ForeignKey("roles.role_id"),
        nullable=False,
        default=UserRoleEnum.DEFAULT.value,
    )

    role = relationship(
        RoleModel,
        backref="users"
    )

    sessions_auth = relationship(
    SessionAuthModel,
    backref="users",
    cascade="all, delete-orphan"
)
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

        from src.data.models import RoleModel

        db: Session = next(DatabaseConfig.get_db())

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
                    user_id=str(uuid.uuid4()),
                    name=cls.__api_user_administrator,
                    email=f"{cls.__api_user_administrator.lower()}@{cls.__api_name}.com",
                    password=AuthUtil.generate_password_hash(
                        cls.__api_password_administrator
                    ),
                    role_id=super_administrator.role_id,
                    created_at=GenUtil.generate_formatted_datetime(),
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
