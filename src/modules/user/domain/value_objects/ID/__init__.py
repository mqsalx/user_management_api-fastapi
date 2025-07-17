# /src/modules/user/domain/value_objects/user_id/__init__.py

import uuid


class ID:
    """
    Class representing a Value Object that wraps and validates a UUID string.

    This class guarantees that any identifier used within the domain
    is a properly formatted UUID, providing type‑safety and consistent
    comparison semantics.
    """

    def __init__(self, value: str) -> None:
        """
        Constructor method that initializes the ID value object,
            validating the supplied UUID.

        Args:
            value (str): A string representation of a UUID.

        Raises:
            ValueError: If the supplied value is not a valid UUID.
        """
        try:
            self._value = str(uuid.UUID(value))
        except ValueError:
            raise ValueError(f"Invalid UUID: {value}")

    @property
    def value(self) -> str:
        """
        Method that returns the internal UUID string.

        Returns:
            str: The canonical (lower‑case, hyphenated) UUID string.
        """
        return self._value

    def __eq__(self, other: object) -> bool:
        """
        Method that compares two ID value objects for equality.

        Args:
            other (object): Another object to compare.

        Returns:
            bool: ``True`` if both objects are `ID` instances
            with the same UUID value, otherwise ``False``.
        """
        return isinstance(other, ID) and self.value == other.value

    def __str__(self) -> str:
        """
        Method that returns the string representation of the UUID.

        Returns:
            str: The UUID string.
        """
        return self.value
