# /src/modules/user/presentation/schemas/request/body/__init__.py

# PY
from pydantic import field_validator

# Domain
from src.domain.dtos.base import BaseDTO
from src.domain.enums import UserStatusEnum

# Modules
from src.modules.user.application.commands import CreateUserCommand


class CreateUserReqBodySchema(BaseDTO):
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

    def to_command(self) -> CreateUserCommand:
        """
        """
        return CreateUserCommand(
            name=self.name,
            email=self.email,
            password=self.password,
            status=self.status.value
        )


class UpdateUserReqBodySchema(BaseDTO):
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
