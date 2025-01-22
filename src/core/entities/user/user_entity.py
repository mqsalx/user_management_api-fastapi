from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.core.enums.user.user_enum import UserStatus


class UserEntity(BaseModel):
    """
    Valida os dados fornecidos, incluindo o tamanho do nome e o status.
    """

    id: Optional[int] = None
    name: str = Field(..., description="Nome do usuário")
    email: str = Field(..., description="Email do usuário")
    status: UserStatus = Field(..., description="Status do usuário")

    @field_validator("name")
    @classmethod
    def validate_name_length(cls, value: str) -> str:
        """
        Valida o tamanho do nome.
        """
        if len(value) < 3:
            raise ValueError("O nome deve ter pelo menos 3 caracteres.")
        if len(value) > 100:
            raise ValueError("O nome não pode ter mais de 100 caracteres.")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        """
        Valida que o status é permitido.
        """
        if value not in UserStatus.__members__.values():
            raise ValueError(
                f"Status '{value}' não é válido. Use um dos seguintes: {', '.join(UserStatus.__members__.values())}"
            )
        return value
