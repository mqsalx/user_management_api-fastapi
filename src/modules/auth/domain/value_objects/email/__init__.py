# /src/modules/auth/domain/value_objects/email/__init__.py

# PY
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """
    Value Object that encapsulates and validates an email address.

    This class ensures that any email used within the domain is well-formed and immutable.
    """

    value: str
    """
    The email address as a string. Must follow a valid format (e.g., user@example.com).
    """

    def __post_init__(self):
        """
        Post-initialization method automatically called after the dataclass constructor.

        This method performs email format validation. If the email is invalid,
        a ValueError is raised.
        """
        if not self.__is_valid_email(self.value):
            raise ValueError("Invalid email format.")

    def __str__(self) -> str:
        """
        Return the string representation of the email.

        Returns:
            str: The email address as a string.
        """
        return self.value

    @staticmethod
    def __is_valid_email(email: str) -> bool:
        """
        Validate the format of the provided email address using a regex pattern.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email has a valid format, False otherwise.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
