# /src/modules/user/infrastructure/mappers/__init__.py

from src.modules.user.domain.entities import UserEntity
from src.modules.user.domain.value_objects import Email, UserId
from src.modules.user.domain.enums import UserRoleEnum, UserStatusEnum
from src.modules.user.infrastructure.models.user import UserModel
from src.shared.infrastructure.mappers.base import BaseMapper


class UserMapper(BaseMapper[UserEntity, UserModel]):
    """
    Class responsible for mapping between the domain entity `User`
    and the ORM model `UserModel`.
    """

    def to_entity(self, model: UserModel) -> UserEntity:
        """
        Convert ORM model to domain entity.

        Args:
            model (UserModel): SQLAlchemy user model.

        Returns:
            User: Domain entity.
        """
        return UserEntity(
            user_id=UserId(model.user_id),
            name=model.name,
            email=Email(model.email),
            password=model.password,
            status=UserStatusEnum(model.status),
            role_id=UserRoleEnum(model.role_id),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def to_model(self, entity: UserEntity) -> UserModel:
        """
        Convert domain entity to ORM model.

        Args:
            entity (User): Domain user entity.

        Returns:
            UserModel: SQLAlchemy model.
        """
        return UserModel(
            user_id=entity.entity_id,
            name=entity.name,
            email=entity.email,
            password=entity.password,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def update_model(self, model: UserModel, entity: UserEntity) -> UserModel:
        model.name = entity.name
        model.email = entity.email
        model.password = entity.password
        model.status = entity.status
        model.updated_at = entity.updated_at
        return model
