# /src/modules/user/domain/repositories/__init__.py

from typing import Optional
from src.shared.domain.repositories.base import BaseAsyncRepository
from src.modules.user.domain.entities import UserEntity


class IUserRepository(BaseAsyncRepository[UserEntity]):
    """
    """

    async def find_by_email(self, email: str) -> Optional[UserEntity]:
        raise NotImplementedError
