# /src/core/dtos/user_dto.py


from typing import Dict, List, Union

from pydantic import EmailStr, RootModel, field_validator

from src.core.dtos.base_dto import BaseDTO
from src.core.enums.user_status_enum import UserStatusEnum


class CreateUserRequestDTO(BaseDTO):
    name: str
    email: EmailStr
    status: UserStatusEnum = UserStatusEnum.ACTIVE
    password: str

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value, info):
        return cls.validate_enum(value, info, UserStatusEnum)


class UpdateUserRequestDTO(BaseDTO):

    __update_mode__ = True

    name: str | None = None
    email: EmailStr | None = None
    status: UserStatusEnum | None = None
    password: str | None = None

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value, info):
        return cls.validate_enum(value, info, UserStatusEnum)


class UserResponseDTO(RootModel):
    root: Union[Dict[str, str], List[Dict[str, str]]]
