# src/shared/infrastructure/mappers/base/__init__.py

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Entity = TypeVar("Entity")
Model = TypeVar("Model")


class BaseMapper(ABC, Generic[Entity, Model]):
    @abstractmethod
    def to_entity(self, model: Model) -> Entity:
        pass

    @abstractmethod
    def to_model(self, entity: Entity) -> Model:
        pass

    @abstractmethod
    def update_model(self, model: Model, entity: Entity) -> Model:
        """
        Updates the model with values from the entity.

        Args:
            model (Model): The ORM model instance to be updated.
            entity (Entity): The domain entity containing new values.

        Returns:
            Model: The updated ORM model instance.
        """
