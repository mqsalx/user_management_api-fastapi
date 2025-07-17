# /src/modules/user/domain/value_objects/status/__init__.py

# Modules
from src.modules.user.domain.enums import UserStatusEnum


class Status:
    """
    Class representing a Value Object that represents the status of a user.

    This class ensures that the status value is one of the predefined
        and valid options defined in the `UserStatusEnum`,
        enforcing domain integrity.
    Class Args:
        value (str): The user status value to be assigned.
    """
    def __init__(self, value: str) -> None:
        """
        Constructor method that initializes the Status object with validation.

        Args:
            value (str): The user status value to be assigned.

        Raises:
            ValueError: If the provided value is not a valid
                member of UserStatusEnum.
        """
        if value not in UserStatusEnum.__members__.values():
            raise ValueError(f"Invalid user status: {value}")
        self._value = value

    @property
    def value(self) -> str:
        """
        Public method that returns the internal value of the status.

        Returns:
            str: The string representation of the user status.
        """
        return self._value

    def __eq__(self, other: object) -> bool:
        """
        Method that compares the current status with another status object.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if both are `Status` instances and have
                the same value, else False.
        """
        return isinstance(other, Status) and self.value == other.value

    def __str__(self) -> str:
        """
        Method that returns the string representation of the status.

        Returns:
            str: The user status as a string.
        """
        return self.value
