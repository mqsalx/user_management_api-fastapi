# /src/modules/user/application/dtos/output/find/by_user_id/__init__.py

from dataclasses import dataclass

from src.modules.user.domain.entities import UserEntity


@dataclass(frozen=True)
class FindUserByUserIdOutput:
    """ """

    name: str
    email: str
    status: str

    @classmethod
    def format(cls, entity: UserEntity) -> "FindUserByUserIdOutput":
        return cls(
            name=entity.name,
            email=entity.email,
            status=entity.status,
        )
