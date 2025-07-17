# /src/modules/user/domain/value_objects/email/__init__.py

import re


class Email:
    """
    Value Object that represents and validates an email address.

    This class encapsulates the logic to validate, compare,
        and represent an email as a strongly-typed
            value object within the domain model.

    Class Args:
        value (str): The email address to be validated and stored.
    """

    def __init__(self, value: str) -> None:
        """
        Constructor method that initializes the Email value object
            and validates the given email string.

        Args:
            value (str): The email address to be validated and stored.

        Raises:
            ValueError: If the provided value is not a valid email format.
        """
        if not self._is_valid(value):
            raise ValueError(f"Invalid email: {value}")
        self.value = value

    def _is_valid(self, value: str) -> bool:
        """
        Private method that checks whether the provided
            string is a valid email address.

        Args:
            value (str): The email string to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        return re.match(r"[^@]+@[^@]+\.[^@]+", value) is not None

    def __str__(self) -> str:
        """
        Method that returns the string representation of the email.

        Returns:
            str: The email address.
        """
        return self.value

    def __eq__(self, other) -> bool:
        """
        Method that compares two Email value objects for equality.

        Args:
            other (Any): Another object to compare.

        Returns:
            bool: True if both are Email instances with the same value.
        """
        return isinstance(other, Email) and self.value == other.value

    def __repr__(self) -> str:
        """
        Method that returns the official string representation
            of the Email object.

        Returns:
            str: The email address.
        """
        return self.value