# /src/shared/infrastructure/repository/base/__init__.py

from abc import abstractmethod
from typing import Generic, List, Optional, Sequence, Tuple, Type, TypeVar

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

# Shared
from src.shared.domain.repositories.base import IBaseAsyncRepository
from src.shared.infrastructure.mappers.base import BaseMapper

Entity = TypeVar("Entity")
Model = TypeVar("Model")


class BaseAsyncRepositoryImpl(
    IBaseAsyncRepository[Entity], Generic[Entity, Model]
):
    """
    Generic asynchronous repository implementation using SQLAlchemy
        and a mapper.

    This class provides a base implementation of common CRUD operations
    for entities using an associated SQLAlchemy model and a mapper for
    transforming between domain entities and database models.

    It is meant to be subclassed, with the `_update_model` method implemented
    to define how to apply updates from the domain entity to the ORM model.

    Class Args:
        async_session_db (AsyncSession): The asynchronous
            SQLAlchemy session.
        model (Type[Model]): The SQLAlchemy model class.
        mapper (BaseMapper): Mapper to convert between domain entity
            and database model.
        entity_id (Optional[str]): The attribute name representing
            the entity's ID.
            If not provided, it is inferred from the model via `id_name()`.
    """

    def __init__(
        self,
        async_session_db: AsyncSession,
        model: Type[Model],
        mapper: BaseMapper[Entity, Model],
        entity_id: Optional[str] = None,
    ) -> None:

        """
        Initializes the repository with a database session, model class,
            and mapper.

        Args:
            async_session_db (AsyncSession): The asynchronous
                SQLAlchemy session.
            model (Type[Model]): The SQLAlchemy model class.
            mapper (BaseMapper): Mapper to convert between domain entity
                and database model.
            entity_id (Optional[str]): The attribute name representing
                the entity's ID.
                If not provided, it is inferred from the model via `id_name()`.
        """
        self._async_session_db: AsyncSession = async_session_db
        self._model: type[Model] = model
        self._mapper: BaseMapper[Entity, Model] = mapper
        self._entity_id: str = (
            entity_id or self._model.id_name()  # type: ignore
        )

    @abstractmethod
    def _update_model(
        self, model: Model, entity: Entity
    ) -> Model:
        """
        Abstract method to update a database model with data from
            a domain entity.

        This method must be implemented in subclasses to define how to copy
        values from the entity into the SQLAlchemy model instance.

        Args:
            model (Model): The existing model instance from the database.
            entity (Entity): The domain entity with updated values.

        Returns:
            Model: The modified model instance.
        """
        pass

    async def create(self, entity: Entity) -> Entity:
        """
        Creates a new entity in the database.

        Args:
            entity (Entity): The domain entity to persist.

        Returns:
            Entity: The created entity, rehydrated from the database.
        """
        model: Model = self._mapper.to_model(entity)
        self._async_session_db.add(model)
        await self._async_session_db.flush()
        await self._async_session_db.refresh(model)
        return self._mapper.to_entity(model=model)

    async def find_by_id(self, entity_id: str) -> Entity | None:
        """
        Finds an entity by its unique identifier.

        Args:
            entity_id (str): The ID of the entity to retrieve.

        Returns:
            Entity | None: The found entity or None if not found.
        """

        stmt: Select[Tuple[Model]] = select(self._model).where(
            getattr(self._model, self._entity_id) == entity_id
        )
        result: Result[Tuple[Model]] = (
            await self._async_session_db.execute(stmt)
        )
        model: Optional[Model] = result.scalars().first()
        return self._mapper.to_entity(model) if model else None

    async def find_all(self) -> List[Entity]:
        """
        Retrieves all entities from the database.

        Returns:
            List[Entity]: A list of all stored entities.
        """
        stmt: Select[Tuple[Model]] = select(self._model)
        result: Result[Tuple[Model]] = (
            await self._async_session_db.execute(stmt)
        )
        models: Sequence[Model] = result.scalars().all()
        return [self._mapper.to_entity(model) for model in models]

    async def update(self, entity: Entity) -> Entity:
        """
        Updates an existing entity in the database.

        Args:
            entity (Entity): The domain entity with updated values.

        Returns:
            Entity: The updated entity.

        Raises:
            ValueError: If the entity does not exist in the database.
        """
        entity_id = getattr(entity, self._entity_id)

        stmt: Select[Tuple[Model]] = select(self._model).where(
            getattr(self._model, self._entity_id) == entity_id
        )
        result: Result[Tuple[Model]] = (
            await self._async_session_db.execute(stmt)
        )
        model: Optional[Model] = result.scalars().first()

        if not model:
            raise ValueError(
                f"Entity with {self._entity_id}={entity_id} not found"
            )

        updated: Model = self._update_model(model, entity)
        await self._async_session_db.flush()
        await self._async_session_db.refresh(updated)
        return self._mapper.to_entity(updated)

    async def remove(self, entity_id: str) -> bool:
        """
        Deletes an entity from the database by its ID.

        Args:
            entity_id (str): The ID of the entity to delete.

        Returns:
            bool: True if the entity was found and deleted, False otherwise.
        """
        stmt: Select[Tuple[Model]] = select(self._model).where(
            getattr(self._model, self._entity_id) == entity_id
        )
        result: Result[Tuple[Model]] = (
            await self._async_session_db.execute(stmt)
        )
        model: Optional[Model] = result.scalars().first()

        if model:
            await self._async_session_db.delete(model)
            await self._async_session_db.flush()
            return True
        return False
