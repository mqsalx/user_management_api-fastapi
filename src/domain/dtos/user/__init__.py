# /src/domain/dtos/user/__init__.py

# flake8: noqa: E501

from typing import Dict, List, Union

from pydantic import (
    ConfigDict,
    EmailStr,
    RootModel,
    field_validator
)

# Core
from src.core.exceptions.dtos import InvalidValueInFieldException

# Domain
from src.domain.dtos.base import BaseDTO
from src.domain.enums import UserStatusEnum


class CreateUserRequestDTO(BaseDTO):
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


class UpdateUserRequestDTO(BaseDTO):
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


class UserResponseDTO(RootModel):
    """
    Class responsible for the Data Transfer Object (DTO) for user-related responses.

    This class structures responses for user-related API calls, returning user details
    as a dictionary or a list of dictionaries.

    Class Args:
        None.
    """

    root: Union[Dict[str, str], List[Dict[str, str]]]


class FindUserByUserIdDTO(BaseDTO):
    """
    Class responsible for the Data Transfer Object (DTO) for retrieving a user by user_id.

    This class validates and structures query parameters used to fetch a specific user,
    ensuring that the required identifier is provided for user-related lookup operations.

    Validation mode: 'query'.

    Class Args:
        None.
    """

    __validation_mode__ = "query"

    user_id: str | None = None

    @field_validator("user_id")
    @classmethod
    def not_blank(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise InvalidValueInFieldException("Query parameter 'user_id' must not be blank or contain only whitespace.")
        return value
