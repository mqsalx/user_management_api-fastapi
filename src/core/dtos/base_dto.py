from enum import Enum
from typing import Any, Type

from pydantic import BaseModel, model_validator

from src.core.exceptions.dto_exception import (
    InvalidExtraFieldsException,
    MissingRequiredFieldsException,
    OnlyAcceptsValuesException,
)
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()


class BaseDTO(BaseModel):

    __update_mode__: bool = False

    @classmethod
    def validate_enum(cls, value: str, info, enum_type: Type[Enum]):
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
