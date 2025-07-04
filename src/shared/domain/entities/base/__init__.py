# /src/shared/domain/entities/base/__init__.py

from uuid import uuid4
from datetime import datetime


class BaseEntity:
    """
    Base class for all domain entities, with built-in ID and timestamp tracking.
    """

    def __init__(
        self,
        entity_id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None
    ) -> None:
        self._entity_id: str = entity_id or str(uuid4())
        self._created_at: datetime = created_at or datetime.now()
        self._updated_at: datetime = updated_at or datetime.now()

    @property
    def id(self) -> str:
        return self._entity_id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at
