# /src/shared/infrastructure/repository/base/__init__.py

from abc import abstractmethod
from typing import Generic, List, Optional, Sequence, Tuple, Type, TypeVar

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

# Shared
from src.shared.domain.repositories.base import BaseAsyncRepository
from src.shared.infrastructure.mappers.base import BaseMapper

DomainEntity = TypeVar("DomainEntity")
DatabaseModel = TypeVar("DatabaseModel")


class BaseAsyncSQLRepository(
    BaseAsyncRepository[DomainEntity], Generic[DomainEntity, DatabaseModel]
):
    """ """

    def __init__(
        self,
        async_session_db: AsyncSession,
        model: Type[DatabaseModel],
        mapper: BaseMapper[DomainEntity, DatabaseModel],
        entity_id: Optional[str] = None,
    ) -> None:
        self._async_session_db: AsyncSession = async_session_db
        self._model: type[DatabaseModel] = model
        self._mapper: BaseMapper[DomainEntity, DatabaseModel] = mapper
        self._entity_id: str = (
            entity_id or self._model.id_name()  # type: ignore
        )

    @abstractmethod
    def _update_model(
        self, model: DatabaseModel, entity: DomainEntity
    ) -> DatabaseModel:
        """ """
        pass

    async def create(self, entity: DomainEntity) -> DomainEntity:
        model: DatabaseModel = self._mapper.to_model(entity)
        self._async_session_db.add(model)
        await self._async_session_db.flush()
        await self._async_session_db.refresh(model)
        return self._mapper.to_entity(model=model)

    async def get_by_id(self, entity_id: str) -> Optional[DomainEntity]:
        stmt: Select[Tuple[DatabaseModel]] = select(self._model).where(
            getattr(self._model, self._entity_id) == entity_id
        )
        result: Result[Tuple[DatabaseModel]] = (
            await self._async_session_db.execute(stmt)
        )
        model: Optional[DatabaseModel] = result.scalars().first()
        return self._mapper.to_entity(model) if model else None

    async def get_all(self) -> List[DomainEntity]:
        stmt: Select[Tuple[DatabaseModel]] = select(self._model)
        result: Result[Tuple[DatabaseModel]] = (
            await self._async_session_db.execute(stmt)
        )
        models: Sequence[DatabaseModel] = result.scalars().all()
        return [self._mapper.to_entity(model) for model in models]

    async def update(self, entity: DomainEntity) -> DomainEntity:
        entity_id = getattr(entity, self._entity_id)

        stmt: Select[Tuple[DatabaseModel]] = select(self._model).where(
            getattr(self._model, self._entity_id) == entity_id
        )
        result: Result[Tuple[DatabaseModel]] = (
            await self._async_session_db.execute(stmt)
        )
        model: Optional[DatabaseModel] = result.scalars().first()

        if not model:
            raise ValueError(
                f"Entity with {self._entity_id}={entity_id} not found"
            )

        updated: DatabaseModel = self._update_model(model, entity)
        await self._async_session_db.flush()
        await self._async_session_db.refresh(updated)
        return self._mapper.to_entity(updated)

    async def delete(self, entity_id: str) -> bool:
        stmt: Select[Tuple[DatabaseModel]] = select(self._model).where(
            getattr(self._model, self._entity_id) == entity_id
        )
        result: Result[Tuple[DatabaseModel]] = (
            await self._async_session_db.execute(stmt)
        )
        model: Optional[DatabaseModel] = result.scalars().first()

        if model:
            await self._async_session_db.delete(model)
            await self._async_session_db.flush()
            return True
        return False
