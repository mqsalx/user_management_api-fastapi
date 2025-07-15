# /src/modules/user/application/dtos/output/update/__init__.py

from dataclasses import dataclass

from src.modules.user.domain.entities import UserEntity


@dataclass(frozen=True)
class UpdateUserOutput:
    """
    """
    user_id: str
    name: str
    email: str
    status: str
    role_id: str

    @classmethod
    def format(cls, entity: UserEntity) -> "UpdateUserOutput":
        """
        Formats the UserEntity into UpdateUserOutput.
        """
        return cls(
            user_id=entity.user_id,
            name=entity.name,
            email=entity.email,
            status=entity.status,
            role_id=entity.role_id,
        )
