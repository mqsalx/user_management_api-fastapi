# /src/modules/user/domain/repositories/__init__.py

# PY
from typing import Optional

# Modules
from src.modules.user.domain.entities import UserEntity

# Shared
from src.shared.domain.repositories.base import IBaseAsyncRepository


class IUserRepository(IBaseAsyncRepository[UserEntity]):
    """
    """

    async def find_by_email(self, email: str) -> Optional[UserEntity]:
        raise NotImplementedError
