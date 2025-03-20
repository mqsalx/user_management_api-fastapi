# /src/core/dtos/user_dto.py


from typing import Dict, List, Union

from pydantic import EmailStr, RootModel, field_validator

from src.core.dtos.base_dto import BaseDTO
from src.core.enums.user_status_enum import UserStatusEnum


class CreateUserRequestDTO(BaseDTO):
    """
    Class responsible for the Data Transfer Object (DTO) for user creation.

    This class is responsible for validating and structuring user creation requests.

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

    Class Attributes:
        name (str, optional): The full name of the user.
        email (EmailStr, optional): The user's email address (must be a valid email format).
        status (UserStatusEnum, optional): The user's account status (default: ACTIVE).
        password (str, optional): The user's password.

    Instance Attributes:
        None
    """

    __update_mode__ = True

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

    Class Attributes:
        None

    Instance Attributes:
        root (Union[Dict[str, str], List[Dict[str, str]]]): The response body,
            which may contain a single user's data or a list of users.
    """

    root: Union[Dict[str, str], List[Dict[str, str]]]
