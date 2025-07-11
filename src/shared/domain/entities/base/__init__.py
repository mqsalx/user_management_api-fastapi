# /src/shared/domain/entities/base/__init__.py

from datetime import datetime
from uuid import uuid4


class BaseEntity:
    """
    Base class for all domain entities, with built-in ID
        and timestamp tracking.

    This class provides foundational attributes and behaviors commonly shared
        across all domain entities, such as a unique identifier (`entity_id`),
        creation timestamp (`created_at`),
        and last update timestamp (`updated_at`).

    It is intended to be extended by specific domain entities within
        the domain layer.

    Class Args:
        entity_id (str | None): Optional UUID string. If not provided,
            one will be generated.
        created_at (datetime | None): Optional creation timestamp.
            Defaults to current datetime.
        updated_at (datetime | None): Optional update timestamp.
            Defaults to current datetime.
    """

    def __init__(
        self,
        entity_id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        """
        Initializes a new instance of BaseEntity.

        Args:
            entity_id (str | None): Optional UUID string. If not provided,
                one will be generated.
            created_at (datetime | None): Optional creation timestamp.
                Defaults to current datetime.
            updated_at (datetime | None): Optional update timestamp.
                Defaults to current datetime.
        """
        self._entity_id: str = entity_id or str(uuid4())
        self._created_at: datetime = created_at or datetime.now()
        self._updated_at: datetime = updated_at or datetime.now()

    @property
    def entity_id(self) -> str:
        """
        Returns the unique identifier of the entity.

        Returns:
            str: UUID string of the entity.
        """
        return self._entity_id

    @property
    def created_at(self) -> datetime:
        """
        Returns the creation timestamp of the entity.

        Returns:
            datetime: Datetime when the entity was created.
        """
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """
        Returns the last update timestamp of the entity.

        Returns:
            datetime: Datetime when the entity was last updated.
        """
        return self._updated_at
