# /src/utils/generator/__init__.py

# flake8: noqa: E501

from datetime import datetime
import random


class GenUtil:
    """
    Class responsible for providing utility functions.

    This class contains static methods for generating formatted timestamps, unique IDs,
    password hashing, and password verification.

    Class Args:
        None
    """

    @staticmethod
    def generate_formatted_datetime() -> str:
        """
        Static method responsible for generating a formatted timestamp.

        This method generates a timestamp formatted as `%y-%m-%d %H:%M:%S`
        for database storage.

        Args:
            None

        Returns:
            str: The formatted timestamp.
        """

        now = datetime.now()
        formatted_datetime = now.strftime("%y-%m-%d %H:%M:%S")
        return formatted_datetime

    @staticmethod
    def generate_unique_id() -> str:
        """
        Static method responsible for generating a unique ID.

        This method generates a unique identifier using the current date-time
        and a randomly generated hexadecimal value.

        Args:
            None

        Returns:
            str: The generated unique ID.
        """

        now = datetime.now()
        sorted_value = random.randint(0, 0xFFFF)
        hex_value = f"{sorted_value:04X}"
        date_time_now = now.strftime("%y%m%d%H%M%S")
        return date_time_now + hex_value
