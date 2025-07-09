# src/shared/infrastructure/mappers/base/__init__.py

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

DomainEntity = TypeVar("DomainEntity")
DatabaseModel = TypeVar("DatabaseModel")


class BaseMapper(ABC, Generic[DomainEntity, DatabaseModel]):
    @abstractmethod
    def to_entity(self, model: DatabaseModel) -> DomainEntity:
        pass

    @abstractmethod
    def to_model(self, entity: DomainEntity) -> DatabaseModel:
        pass
