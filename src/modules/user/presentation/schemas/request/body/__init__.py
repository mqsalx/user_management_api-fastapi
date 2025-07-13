# /src/modules/user/presentation/schemas/request/body/__init__.py

# PY
from pydantic import field_validator

# Modules
from src.modules.user.domain.enums import UserStatusEnum

# Shared
from src.shared.presentation.schemas.base import BaseSchema


class CreateUserReqBodySchema(BaseSchema):
    """
    Class responsible for the Data Transfer Object (DTO) for user creation.

    This class is responsible for validating
        and structuring user creation requests.

    Validation mode: 'create'.

    Class Args:
        None
    """

    name: str
    email: str
    status: UserStatusEnum = UserStatusEnum.ACTIVE
    password: str

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value, info) -> str:
        """
        Class method that validates if the given value
            is a valid UserStatusEnum member.

        Args:
            value: The value to be validated.
            info: Field metadata provided by Pydantic.

        Returns:
            str: The validated status value.
        """
        return cls.validate_enum(value, info, UserStatusEnum)


class UpdateUserReqBodySchema(BaseSchema):
    """
    Class responsible for the Data Transfer Object (DTO) for user update.

    This class is responsible for validating and structuring user update requests.

    Validation mode: 'update'.

    Class Args:
        None
    """

    __validation_mode__ = "update"

    name: str | None = None
    email: str | None = None
    status: UserStatusEnum | None = None
    password: str | None = None
    role_id: str | None = None

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
