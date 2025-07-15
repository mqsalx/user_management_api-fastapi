# /src/modules/user/domain/value_objects/user_id/__init__.py

import uuid


class UserId:
    """
    """
    def __init__(self, value: str):
        try:
            self._value = str(uuid.UUID(value))
        except ValueError:
            raise ValueError(f"Invalid UUID: {value}")

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UserId) and self.value == other.value

    def __str__(self) -> str:
        return self.value
