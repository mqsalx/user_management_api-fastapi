# /src/shared/domain/unit_of_work/__init__.py

from abc import ABC, abstractmethod


class IAsyncUnitOfWork(ABC):
    """
    Interface for asynchronous Unit of Work implementations.
    """

    @abstractmethod
    async def __aenter__(self) -> "IAsyncUnitOfWork":
        """Enter the async context."""
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the async context, committing or rolling back as needed."""
        pass

    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction."""
        pass

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction."""
        pass
