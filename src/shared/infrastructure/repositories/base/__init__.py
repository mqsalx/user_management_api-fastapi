# /src/shared/infrastructure/repository/base/__init__.py

from typing import Generic, List, Optional, Sequence, Tuple, Type, TypeVar

from sqlalchemy import Result, Select, asc, desc, func, select
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

    async def find_all(
        self,
        total_count: bool = False,
        offset: int | None = None,
        limit: int | None = None,
        order: str | None = None,
    ) -> int | List[Entity]:
        """
        Retrieves all entities from the database.

        Returns:
            List[Entity]: A list of all stored entities.
        """

        if total_count:
            count_stmt = select(func.count()).select_from(self._model)
            result = await self._async_session_db.execute(count_stmt)
            return result.scalar_one()

        order_by = (
            asc(getattr(self._model, self._entity_id))
            if order.lower() == "asc"
            else desc(getattr(self._model, self._entity_id))
        )

        stmt: Select = (
            select(self._model).order_by(order_by).offset(offset).limit(limit)
        )

        result = await self._async_session_db.execute(stmt)

        models: Sequence[Model] = result.scalars().all()

        return [self._mapper.to_entity(model) for model in models]

    async def find_by_entity_id(self, entity_id: str) -> Entity | None:
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
        result: Result[Tuple[Model]] = await self._async_session_db.execute(
            stmt
        )
        model: Optional[Model] = result.scalars().first()
        return self._mapper.to_entity(model) if model else None

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

        if hasattr(entity_id, "value"):
            entity_id = entity_id.value

        stmt: Select[Tuple[Model]] = select(self._model).where(
            getattr(self._model, self._entity_id) == entity_id
        )

        result: Result[Tuple[Model]] = await self._async_session_db.execute(
            stmt
        )

        model: Optional[Model] = result.scalars().first()

        if not model:
            raise ValueError(f"Entity with {entity_id} not found")

        to_update: Model = self._mapper.update_model(
            model=model, entity=entity
        )

        await self._async_session_db.flush()

        await self._async_session_db.refresh(to_update)

        return self._mapper.to_entity(to_update)

    async def remove(self, entity_id: str) -> bool:
        """
        Deletes an entity from the database by its ID.

        Args:
            entity_id (str): The ID of the entity to delete.

        Returns:
            bool: True if the entity was found and deleted, False otherwise.
        """
        stmt: Select[Tuple[Model]] = select(self._model).where(
            getattr(self._model, self._entity_id) == str(entity_id)
        )
        result: Result[Tuple[Model]] = await self._async_session_db.execute(
            stmt
        )
        model: Optional[Model] = result.scalars().first()

        if model:
            await self._async_session_db.delete(model)
            await self._async_session_db.flush()
            return True
        return False
