# /src/domain/dtos/request/body/user/__init__.py

# flake8: noqa: E501

# PY
from pydantic import (
    EmailStr,
    field_validator
)

# Domain
from src.domain.dtos.base import BaseDTO
from src.domain.enums import UserStatusEnum


class CreateUserReqBodyDTO(BaseDTO):
    """
    Class responsible for the Data Transfer Object (DTO) for user creation.

    This class is responsible for validating and structuring user creation requests.

    Validation mode: 'create'.

    Class Args:
        None
    """

    name: str
    email: EmailStr
    status: UserStatusEnum = UserStatusEnum.ACTIVE
    password: str

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value, info) -> str:
        """
        Class method that validates if the given value is a valid UserStatusEnum member.

        Args:
            value: The value to be validated.
            info: Field metadata provided by Pydantic.

        Returns:
            str: The validated status value.
        """
        return cls.validate_enum(value, info, UserStatusEnum)
