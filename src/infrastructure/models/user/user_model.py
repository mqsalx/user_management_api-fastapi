# /src/infrastructure/models/user/user_model.py

from sqlalchemy import Column, Enum, Integer, String

from src.core.enums.user.user_enum import UserStatusEnum
from src.infrastructure.db.database_configuration import DatabaseConfiguration


class UserModel(DatabaseConfiguration.base()):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    # password = Column(String, nullable=False)
    status = Column(
        Enum(UserStatusEnum), nullable=False, default=UserStatusEnum.ACTIVE
    )
