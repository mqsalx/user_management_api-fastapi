# /src/modules/user/presentation/dependencies/database/__init__.py

# PY
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Core
from src.core.configurations.database import db_config

# Modules
from src.modules.user.domain.repositories import IUserRepository
from src.modules.user.infrastructure.repositories import UserRepositoryImpl


class Dependencies:
    """ """

    @staticmethod
    async def get_user_repository(
        async_db_session: AsyncSession = Depends(
            dependency=db_config.get_async_db
        ),
    ) -> IUserRepository:
        """ """
        return UserRepositoryImpl(async_db_session=async_db_session)


dependencies = Dependencies()
