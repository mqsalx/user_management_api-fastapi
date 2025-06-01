# /src/domain/dtos/user/__init__.py

# flake8: noqa: E501

# Domain
from pydantic import EmailStr, field_validator

from src.domain.enums.user import UserStatusEnum
from src.domain.dtos.base import BaseDTO


class RemoveUserByUserIdReqPathDTO(BaseDTO):
    """
    Class responsible for the Data Transfer Object (DTO) for user creation.

    This class is responsible for validating and structuring user creation requests.

    Validation mode: 'create'.

    Class Args:
        None
    """

    user_id: str


class UpdateUserReqPathDTO(BaseDTO):
    """
    Class responsible for the Data Transfer Object (DTO) for user update.

    This class is responsible for validating and structuring user update requests.

    Validation mode: 'update'.

    Class Args:
        None
    """

    __validation_mode__ = "update"

    name: str | None = None
    email: EmailStr | None = None
    status: UserStatusEnum | None = None
    password: str | None = None

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
