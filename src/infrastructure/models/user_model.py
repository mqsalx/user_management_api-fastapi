# /src/infrastructure/models/user_model.py

from sqlalchemy import Column, Enum, Integer, String

from src.core.enums.user_role_enum import UserRoleEnum
from src.core.enums.user_status_enum import UserStatusEnum
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)
from src.utils.any_utils import AnyUtils

Base = DatabaseConfiguration.base()


class UserModel(Base):

    __tablename__ = "users"

    _prefix_id = "U"
    _custom_id = f"{_prefix_id}{AnyUtils.generate_unique_id()}"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False, default=_custom_id)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    status = Column(
        Enum(UserStatusEnum), default=UserStatusEnum.ACTIVE, nullable=False
    )
    role = Column(
        Enum(UserRoleEnum), default=UserRoleEnum.DEFAULT, nullable=True
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
