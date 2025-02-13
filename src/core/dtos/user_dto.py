# /src/core/dtos/user_dto.py


from typing import Dict, List, Union

from pydantic import BaseModel, EmailStr, RootModel

from src.core.enums.user_enum import UserStatusEnum


class UserRequestDTO(BaseModel):
    name: str
    email: EmailStr
    status: UserStatusEnum = UserStatusEnum.ACTIVE


class UserResponseDTO(RootModel):
    root: Union[Dict[str, str], List[Dict[str, str]]]
