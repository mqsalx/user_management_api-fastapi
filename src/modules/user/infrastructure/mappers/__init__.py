# /src/modules/user/infrastructure/mappers/__init__.py

# PY
import datetime
from dataclasses import fields
from enum import Enum

# Modules
from src.modules.user.domain.entities import UserEntity
from src.modules.user.domain.enums import UserRoleEnum, UserStatusEnum
from src.modules.user.domain.value_objects import Email, ID
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
            user_id=str(model.user_id),
            # user_id=UserId(model.user_id),
            name=model.name,
            email=str(model.email),
            # email=Email(model.email),
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
            user_id=entity.user_id,
            name=entity.name,
            email=entity.email,
            password=entity.password,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def update_model(self, model: UserModel, entity: UserEntity) -> UserModel:
        """
        Updates a UserModel instance with values from a UserEntity,
        ignoring immutable fields like 'id' and 'created_at'.

        Args:
            model (UserModel): The existing ORM model from the database.
            entity (UserEntity): The domain entity containing updated values.

        Returns:
            UserModel: The updated ORM model ready for persistence.
        """
        IMMUTABLE_FIELDS = {"id", "created_at", "user_id"}

        for field in fields(entity):
            field_name: str = field.name

            if field_name in IMMUTABLE_FIELDS or not hasattr(
                model, field_name
            ):
                continue

            new_value = getattr(entity, field_name)

            if isinstance(new_value, Enum):
                new_value = new_value.value
            elif isinstance(new_value, datetime.datetime):
                pass
            elif not isinstance(new_value, (str, int, float, bool)):
                new_value = str(new_value)

            current_value = getattr(model, field_name, None)

            if new_value != current_value:
                setattr(model, field_name, new_value)

        return model
