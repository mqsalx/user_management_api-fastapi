# /app/models/user_models.py

from sqlalchemy import Column, Enum, Integer, String

from dtos.user.user_dto import UserStatus
from src.infrastructure.database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    status = Column(
        Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE
    )
