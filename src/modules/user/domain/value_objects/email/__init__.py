# /src/modules/user/domain/value_objects/email/__init__.py

import re


class Email:
    def __init__(self, value: str):
        if not self._is_valid(value):
            raise ValueError(f"Invalid email: {value}")
        self.value = value

    def _is_valid(self, value: str) -> bool:
        return re.match(r"[^@]+@[^@]+\.[^@]+", value) is not None

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other) -> bool:
        return isinstance(other, Email) and self.value == other.value

    def __repr__(self) -> str:
        return self.value
