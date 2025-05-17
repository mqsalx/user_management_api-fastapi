# /src/domain/dtos/base/__init__.py

# flake8: noqa: E501

from enum import Enum
from typing import Any, Type

from pydantic import BaseModel, model_validator

from src.core.exceptions.dtos import (
    InvalidExtraFieldsException,
    MissingRequiredFieldsException,
    OnlyAcceptsValuesException,
)

from src.utils import LoggerUtil

log = LoggerUtil()


class BaseDTO(BaseModel):
    """
    Class responsible for the Data Transfer Object (DTO) for request validation.

    This class serves as the base DTO for other models, providing validation methods
    to ensure proper field handling and enumerations.

    Class Args:
        None
    """

    __update_mode__: bool = False

    @classmethod
    def validate_enum(cls, value: str, info, enum_type: Type[Enum]) -> str:
        """
        Class method that validates if the given value is a valid enum member.

        Ensures that the provided value is a valid option within the specified Enum type.

        Args:
            value (str): The value to be validated against the Enum.
            info: Field information provided by Pydantic.
            enum_type (Type[Enum]): The Enum class against which validation is performed.

        Returns:
            str: The validated enum value.

        Raises:
            OnlyAcceptsValuesException: If the value is empty or not a valid enum member.
        """

        field_name = info.field_name
        allowed_values = {role.value for role in enum_type}

        if value in ["", " "]:
            raise OnlyAcceptsValuesException(
                f"The field {field_name} was given empty or null value! Allowed values: {', '.join(allowed_values)}"
            )

        if value not in allowed_values:
            raise OnlyAcceptsValuesException(
                f"The field {field_name} was given {value}, which is invalid! Allowed values: {', '.join(allowed_values)}"
            )

        return value

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, values: Any) -> Any:
        """
        Class method that validates extra and missing fields before model creation.

        Ensures that no extra fields are provided and that all required fields are present
        unless `__update_mode__` is enabled.

        Args:
            values (Any): Dictionary containing the fields provided in the request.

        Returns:
            Any: The validated values if they conform to the expected model.

        Raises:
            InvalidExtraFieldsException: If additional fields not defined in the DTO are provided.
            MissingRequiredFieldsException: If required fields are missing when `__update_mode__` is disabled.
        """

        allowed_fields = set(cls.model_fields.keys())
        received_fields = set(values.keys())

        extra_fields = received_fields - allowed_fields

        if extra_fields:
            raise InvalidExtraFieldsException(
                f'Additional fields not allowed: {", ".join(extra_fields)}'
            )

        if not cls.__update_mode__:
            missing_fields = allowed_fields - received_fields
            if missing_fields:
                raise MissingRequiredFieldsException(
                    f'Required fields missing: {", ".join(missing_fields)}'
                )

        return values
