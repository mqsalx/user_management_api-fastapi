# /src/dtos/user/user_dto.py


from pydantic import BaseModel, ConfigDict, EmailStr

from src.core.enums.user.user_enum import UserStatusEnum


class UserRequestDTO(BaseModel):
    name: str
    email: EmailStr
    status: UserStatusEnum = UserStatusEnum.ACTIVE

    model_config = ConfigDict(extra="forbid")


class UserResponseDTO(BaseModel):
    id: int
    name: str
    email: EmailStr
    status: UserStatusEnum
    created_at: str

    model_config = ConfigDict(from_attributes=True)
