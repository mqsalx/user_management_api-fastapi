# /src/modules/user/domain/repositories/__init__.py

# PY
from abc import abstractmethod
from typing import Optional

# Modules
from src.modules.user.domain.entities import UserEntity

# Shared
from src.shared.domain.repositories.base import IBaseAsyncRepository


class IUserRepository(IBaseAsyncRepository[UserEntity]):
    """
    Class representing an interface for user-specific repository operations.

    Extends the base asynchronous repository with additional methods
    for querying user-specific attributes such as email.

    This interface defines the contract that any user repository implementation
    must follow to support domain-level operations related to user entities.
    """

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[UserEntity]:
        """
        Abstract method to retrieve a user entity based on its email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            Optional[UserEntity]: The user entity if found, otherwise None.
        """
        pass
