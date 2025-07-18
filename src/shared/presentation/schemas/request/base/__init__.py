# /src/shared/presentation/schemas/base/__init__.py

from fastapi import Body, Depends, FastAPI, Path, Query

from enum import Enum
from typing import Any, Literal, Type

from pydantic import BaseModel, model_validator

from src.core.exceptions.dtos import (
    InvalidExtraFieldsException,
    MissingRequiredFieldsException,
    OnlyAcceptsValuesException,
)
from src.utils import log


class BaseRequest(BaseModel):
    """
    Class responsible for the Schemas for request validation.

    This class serves as the base DTO for other models,
        providing validation methods
        to ensure proper field handling and enumerations.

    With support for contextual validation:
        - 'create': all required fields must be present and non-null
        - 'update': partial updates allowed (no required fields enforced)
        - 'query': required fields must be present; optional
            fields must have defaults
    """
    __request_type__: Literal["body", "query", "path"] = "body"
    __action_type__: Literal["create", "update", "find", "delete"] = "create"

    @classmethod
    def validate_enum(cls, value: str, info, enum_type: Type[Enum]) -> str:
        """
        Class method that validates if the given value is a valid enum member.

        Ensures that the provided value is a valid option within
            the specified Enum type.

        Args:
            value (str): The value to be validated against the Enum.
            info: Field information provided by Pydantic.
            enum_type (Type[Enum]): The Enum class against which
                validation is performed.

        Returns:
            str: The validated enum value.

        Raises:
            OnlyAcceptsValuesException: If the value is empty
                or not a valid enum member.
        """

        field_name = info.field_name
        allowed_values = {role.value for role in enum_type}

        if value in ["", " "]:
            raise OnlyAcceptsValuesException(
                f"The field {field_name} was given empty or null value! Allowed values: {', '.join(allowed_values)}"  # noqa: E501
            )

        if value not in allowed_values:
            raise OnlyAcceptsValuesException(
                f"The field {field_name} was given {value}, which is invalid! Allowed values: {', '.join(allowed_values)}"  # noqa: E501
            )

        return value

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, values: Any) -> Any:
        """
        Class method that validates extra and missing fields
            before model creation.

        Ensures that no extra fields are provided and that all required
            fields are present unless `__update_mode__` is enabled.

        Args:
            values (Any): Dictionary containing the fields
                provided in the request.

        Returns:
            Any: The validated values if they conform to the expected model.

        Raises:
            InvalidExtraFieldsException: If additional fields not defined
                in the DTO are provided.
            MissingRequiredFieldsException: If required fields are missing
                when `__update_mode__` is disabled.
        """
        allowed_fields = set(cls.model_fields.keys())
        received_fields = set(values.keys())

        extra_fields = received_fields - allowed_fields
        if extra_fields:
            raise InvalidExtraFieldsException(
                f"Additional fields not allowed: {', '.join(extra_fields)}"
            )

        action = getattr(cls, "__action_type__", "create")

        if action == "create" or action == "delete":
            missing_fields = []
            for field_name, field in cls.model_fields.items():
                value = values.get(field_name)
                if isinstance(value, str):
                    sanitized = value.strip().strip('"').strip()
                    if sanitized == "":
                        raise OnlyAcceptsValuesException(
                            f"The field '{field_name}' was given an empty or whitespace-only value!"  # noqa: E501
                        )
                if field.is_required and (
                    field_name not in values or values.get(field_name) is None
                ):
                    missing_fields.append(field_name)
            if missing_fields:
                raise MissingRequiredFieldsException(
                    f"Required fields missing: {', '.join(missing_fields)}"  # noqa: E501
                )

        elif action == "query":

            default_query_params: dict = {
                "page": 1,
                "limit": 1,
                "order": "asc",
            }

            for field, default_value in default_query_params.items():
                value = values.get(field)

                if (
                    value is None
                    or field not in values
                    or (isinstance(value, (int, float)) and value <= 0)
                ):
                    values[field] = default_value

            # Order Field Validation
            if str(values.get("order", "")).lower() not in {"asc", "desc"}:
                values["order"] = default_query_params["order"]

            invalid_fields = []

            for field_name, field in cls.model_fields.items():
                value = values.get(field_name)
                if isinstance(value, str):
                    sanitized = value.strip().strip('"').strip()
                    if sanitized == "":
                        raise OnlyAcceptsValuesException(
                            f"The field '{field_name}' was given an empty or whitespace-only value!"  # noqa: E501
                        )
                is_present = field_name in values
                is_required = field.is_required
                has_default = (
                    field.default is not None
                    or field.default_factory is not None
                )

            if is_required and not is_present and not has_default:
                invalid_fields.append(field_name)

            if invalid_fields:
                log.warning(
                    f"[{cls.__name__}] invalid fields detected in query mode: {invalid_fields}"  # noqa: E501
                )
                raise MissingRequiredFieldsException(
                    f"In query mode, these fields are required or must have defaults: {', '.join(invalid_fields)}"  # noqa: E501
                )

        return values
