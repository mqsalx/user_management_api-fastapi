# /src/modules/user/infrastructure/mappers/__init__.py

from src.modules.user.domain.entities.user import User
from src.modules.user.domain.value_objects import Email, UserId
from src.modules.user.enums import UserStatusEnum, UserRoleEnum
from src.modules.user.infrastructure.models.user_model import UserModel


class UserMapper:
    """
    Class responsible for mapping between the domain entity `User`
    and the ORM model `UserModel`.
    """

    def to_entity(self, model: UserModel) -> User:
        """
        Convert ORM model to domain entity.

        Args:
            model (UserModel): SQLAlchemy user model.

        Returns:
            User: Domain entity.
        """
        return User(
            user_id=UserId(model.user_id),
            name=model.name,
            email=Email(model.email),
            password=model.password,
            status=UserStatusEnum(model.status),
            role=UserRoleEnum(model.role_id),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def to_model(self, entity: User) -> UserModel:
        """
        Convert domain entity to ORM model.

        Args:
            entity (User): Domain user entity.

        Returns:
            UserModel: SQLAlchemy model.
        """
        return UserModel(
            user_id=entity.user_id.value,
            name=entity.name,
            email=str(entity.email),
            password=entity.password,
            status=entity.status,
            role_id=entity.role.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
