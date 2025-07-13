# /src/shared/domain/repositories/base/__init__.py

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class IBaseAsyncRepository(ABC, Generic[T]):
    """
    Base interface for an asynchronous repository.

    Defines the contract for standard CRUD operations to be implemented
    by all concrete asynchronous repository classes, using a generic
    domain entity type `T`.
    """

    @abstractmethod
    async def create(self, entity: T) -> T:
        """
        Persists a new entity asynchronously.

        Args:
            entity (T): The entity instance to be created.

        Returns:
            T: The newly created entity, possibly with
                updated fields (e.g., generated ID).
        """

    @abstractmethod
    async def find_by_entity_id(self, entity_id: str) -> Optional[T]:
        """
        Retrieves an entity by its unique identifier.

        Args:
            entity_id (str): The unique identifier of the entity.

        Returns:
            Optional[T]: The found entity, or None if not found.
        """

    @abstractmethod
    async def find_all(
        self,
        total_count: bool = False,
        offset: int | None = None,
        limit: int | None = None,
        order: str | None = None,
    ) -> int | List[T]:
        """
        Retrieves all entities of this type.

        Returns:
            List[T]: A list of all entities stored in the repository.
        """

    @abstractmethod
    async def update(self, entity: T) -> T:
        """
        Updates an existing entity in the repository.

        Args:
            entity (T): The entity instance with updated data.

        Returns:
            T: The updated entity after persistence.
        """

    @abstractmethod
    async def remove(self, entity_id: str) -> bool:
        """
        Deletes an entity by its unique identifier.

        Args:
            entity_id (str): The unique identifier of the entity to be removed.

        Returns:
            bool: True if the entity was successfully deleted, False otherwise.
        """
