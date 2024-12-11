# /app/dtos/user_dto.py

from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class UserCreateDTO(BaseModel):
    name: str
    email: EmailStr
    status: UserStatus = UserStatus.ACTIVE

    model_config = ConfigDict(extra="forbid")


class UserResponseDTO(BaseModel):
    id: int
    name: str
    email: EmailStr
    status: UserStatus

    model_config = ConfigDict(from_attributes=True)
