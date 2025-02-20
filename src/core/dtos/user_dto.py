# /src/core/dtos/user_dto.py


from typing import Dict, List, Union

from pydantic import BaseModel, EmailStr, RootModel

from src.core.enums.user_status_enum import UserStatusEnum


class CreateUserRequestDTO(BaseModel):
    name: str
    email: EmailStr
    status: UserStatusEnum = UserStatusEnum.ACTIVE
    password: str


class UpdateUserRequestDTO(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    status: UserStatusEnum | None = None
    password: str | None = None


class UserResponseDTO(RootModel):
    root: Union[Dict[str, str], List[Dict[str, str]]]
