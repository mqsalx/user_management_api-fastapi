# /src/modules/user/domain/value_objects/status/__init__.py

# Modules
from src.modules.user.domain.enums import UserStatusEnum


class Status:
    def __init__(self, value: str):
        if value not in UserStatusEnum.__members__.values():
            raise ValueError(f"Invalid user status: {value}")
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Status) and self.value == other.value

    def __str__(self) -> str:
        return self.value
