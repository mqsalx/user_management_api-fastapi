from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseEntity:
    """
    Base entity with ID, creation and update timestamps.
    """
    entity_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
