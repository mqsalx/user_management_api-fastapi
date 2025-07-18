# /src/shared/presentation/dependencies/base/__init__.py

# PY
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Core
from src.core.configurations.database import db_config

# Shared
from src.shared.infrastructure.unit_of_work import AsyncUnitOfWork


class BaseDependency:
    """
    Base class responsible for providing dependencies related
        to user components.

    This class centralizes dependency injection logic for FastAPI,
        enabling the injection of core services such as repositories
            and unit of work instances into routes,
    controllers, and use cases via FastAPI's `Depends` mechanism.

    All dependencies rely on an asynchronous database session
        provided by the application,
        ensuring transactional consistency in asynchronous workflows.
    """

    @staticmethod
    async def get_async_unit_of_work(
        async_session_db: AsyncSession = Depends(
            dependency=db_config.get_async_db
        ),
    ) -> AsyncUnitOfWork:
        """
        Provides an instance of AsyncUnitOfWork for managing
            database transactions.

        This method is designed to be used with FastAPI's
            dependency injection system to ensure consistent transaction
            handling within the application layer.

        Args:
            async_session_db (AsyncSession): The asynchronous SQLAlchemy
                session used for executing database operations.

        Returns:
            AsyncUnitOfWork: A concrete implementation of the
                unit of work pattern for asynchronous database interactions.
        """
        return AsyncUnitOfWork(async_session_db=async_session_db)
