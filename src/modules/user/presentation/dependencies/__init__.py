# /src/modules/user/presentation/dependencies/database/__init__.py

# PY
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Core
from src.core.configurations.database import db_config

# Modules
from src.modules.user.domain.repositories import IUserRepository
from src.modules.user.infrastructure.repositories import UserRepositoryImpl

# Shared
from src.shared.presentation.dependencies.base import BaseDependency


class UserDependency(BaseDependency):
    """
    Static dependency providers for user-related components.

    This class centralizes the dependency injection logic for FastAPI, allowing
        services like the user repository and unit of work
        to be injected into routes  and controllers using FastAPI's `Depends`.

    The dependencies rely on an asynchronous database session
        provided by the application.
    """

    @staticmethod
    async def get_user_repository(
        async_session_db: AsyncSession = Depends(
            dependency=db_config.get_async_db
        ),
    ) -> IUserRepository:
        """
        Provides an instance of IUserRepository with an async database session.

        This method is intended to be used with FastAPI's dependency
            injection system.

        Args:
            async_session_db (AsyncSession): The asynchronous
                SQLAlchemy session.

        Returns:
            IUserRepository: An instance of the user repository implementation.
        """
        return UserRepositoryImpl(async_session_db=async_session_db)
