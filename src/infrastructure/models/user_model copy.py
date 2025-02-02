# /src/infrastructure/models/user_model.py

from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.core.enums.user.user_enum import UserStatusEnum


class UserModelOLD(BaseModel):

    id: Optional[str] = None
    name: str = Field(..., description="User name")
    email: str = Field(..., description="User email")
    status: UserStatusEnum = Field(..., description="User status")

    @field_validator("name")
    @classmethod
    def validate_name_length(cls, value: str) -> str:
        """
        Validate name length.
        """
        if len(value) < 3:
            raise ValueError("The name must be at least 3 characters long.")
        if len(value) > 100:
            raise ValueError("The name cannot be longer than 100 characters.")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        """
        Validates that the status is allowed.
        """
        if value not in UserStatusEnum.__members__.values():
            raise ValueError(
                f"Status '{value}' is not valid. Use one of the following: {', '.join(UserStatusEnum.__members__.values())}"
            )
        return value
