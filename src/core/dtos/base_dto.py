from enum import Enum
from typing import Any

from pydantic import (
    BaseModel,
    ValidationInfo,
    field_validator,
    model_validator,
)

from src.core.exceptions.dto_exception import (
    InvalidExtraFieldsException,
    MissingRequiredFieldsException,
    OnlyAcceptsValuesException,
)


class BaseDTO(BaseModel):

    @field_validator("*", mode="before")
    @classmethod
    def validate_enum(cls: Any, value: Any, info: ValidationInfo) -> Any:

        field = info.field_name
        field_type = cls.model_fields[field].annotation

        if isinstance(field_type, type) and issubclass(field_type, Enum):
            allowed_values = [e.value for e in field_type]
            if value not in allowed_values:
                if value is None or value == "":
                    value = "empty or null"
                raise OnlyAcceptsValuesException(
                    f"The {field} field received {value}! Allowed values: {", ".join(allowed_values)}"
                )

        return value

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, values: Any) -> Any:
        allowed_fields = set(cls.model_fields.keys())
        received_fields = set(values.keys())

        extra_fields = received_fields - allowed_fields
        missing_fields = allowed_fields - received_fields

        if extra_fields:
            raise InvalidExtraFieldsException(
                f'Additional fields not allowed: {", ".join(extra_fields)}'
            )

        if missing_fields:
            raise MissingRequiredFieldsException(
                f'Required fields missing: {", ".join(missing_fields)}'
            )

        return values
