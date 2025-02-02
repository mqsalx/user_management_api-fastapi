# /src/infrastructure/models/user_model.py

from sqlalchemy import Column, Enum, Integer, String

from src.core.enums.user.user_enum import UserStatusEnum
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)

Base = DatabaseConfiguration.base()


class UserModel(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    status = Column(
        Enum(UserStatusEnum), default=UserStatusEnum.ACTIVE, nullable=False
    )
    created_at = Column(String, nullable=False)
