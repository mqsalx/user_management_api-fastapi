# /src/modules/user/application/dtos/output/create/__init__.py

# PY
from dataclasses import dataclass

from src.modules.user.domain.entities import UserEntity

@dataclass
class CreateUserOutput:
    """
    """
    user_id: str
    name: str
    email: str
    password: str
    status: str
    role_id: str

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "CreateUserOutput":
        return cls(
            user_id=entity.user_id,
            name=entity.name,
            email=entity.email,
            status=entity.status,
            password=entity.password,
            role_id=entity.role_id,
        )
