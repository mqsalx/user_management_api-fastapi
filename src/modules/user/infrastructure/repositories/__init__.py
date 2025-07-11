# /src/modules/user/infrastructure/repositories/__init__.py

# PY
from typing import Optional, Tuple

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

# Modules
from src.modules.user.domain import IUserRepository, UserEntity
from src.modules.user.infrastructure.mappers import UserMapper
from src.modules.user.infrastructure.models.user import UserModel

# Shared
from src.shared.infrastructure.repositories.base import BaseAsyncRepositoryImpl


class UserRepositoryImpl(
    BaseAsyncRepositoryImpl[UserEntity, UserModel], IUserRepository
):
    """
    Class responsible for handling database operations
        related to user management.

    This repository provides methods for creating,
        retrieving, and deleting users.

    Class Args:
        async_session_db (AsyncSession): The database async session
            used for executing queries.
    """

    def __init__(self, async_session_db: AsyncSession) -> None:
        """
        Constructor method for UserRepository.

        Initializes the repository with a database session.

        Args:
            async_session_db (AsyncSession): The database async session
                used for executing queries.
        """
        super().__init__(
            async_session_db=async_session_db,
            model=UserModel,
            mapper=UserMapper(),
        )

    def _update_model(self, model: UserModel, entity: UserEntity) -> UserModel:
        """ """
        model.name = entity.name
        model.email = entity.email
        model.password = entity.password
        model.status = entity.status
        model.updated_at = entity.updated_at
        return model

    async def find_by_email(self, email: str) -> Optional[UserEntity]:
        """
        Public method responsible for retrieving a user by their email.

        This method queries the database to find
            a user with the specified email address.

        Args:
            email (str): The email address of the user.

        Returns:
            UserModel | None: The user matching the email if found,
                otherwise None.
        """

        stmt: Select[Tuple[UserModel]] = select(self._model).where(
            self._model.email == email
        )
        result: Result[Tuple[UserModel]] = (
            await self._async_session_db.execute(stmt)
        )
        model: UserModel | None = result.scalars().first()
        return self._mapper.to_entity(model) if model else None
