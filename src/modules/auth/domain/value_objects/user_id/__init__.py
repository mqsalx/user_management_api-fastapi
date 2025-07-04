# /src/modules/auth/domain/value_objects/user_id/__init__.py

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class UserId:
    """
    Value Object that represents a unique identifier for a User.

    This class ensures that every identifier used for a User is a valid UUID.
    It accepts an existing UUID, a UUID string, or generates a new one automatically
    if no value is provided.
    """

    value: UUID
    """
    The internal UUID value representing the user's identity.
    """

    def __init__(self, value: str | UUID | None = None):
        """
        Initialize the UserId value object.

        Args:
            value (str | UUID | None): A UUID instance, a UUID string,
                or None to auto-generate a new UUID.

        Raises:
            ValueError: If the provided value is not a valid UUID format.
        """
        object.__setattr__(self, "value", self.__validate(value))

    def __str__(self) -> str:
        """
        Return the string representation of the UUID.

        Returns:
            str: UUID in string format.
        """
        return str(self.value)

    @staticmethod
    def __validate(value: str | UUID | None) -> UUID:
        """
        Validate and convert the input value to a UUID.

        Args:
            value (str | UUID | None): Input that should represent a UUID.

        Returns:
            UUID: A valid UUID object.

        Raises:
            ValueError: If the value is not a valid UUID.
        """
        if value is None:
            return uuid4()

        if isinstance(value, UUID):
            return value

        try:
            return UUID(str(value))
        except ValueError:
            raise ValueError("Invalid UUID format for UserId.")
