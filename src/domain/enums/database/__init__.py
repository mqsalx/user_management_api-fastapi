# /src/domain/enums/database/__init__.py

# flake8: noqa: E501

from enum import Enum


class DatabaseTypeEnum(str, Enum):
    """
    Enumerated class for supported database types.

    This enum defines the possible database engines that can be used in the application.

    Class Args:
        None

    Members:
        POSTGRESQL (str): Represents a PostgreSQL database.
        MYSQL (str): Represents a MySQL database.
        SQLITE (str): Represents an SQLite database.
    """

    POSTGRESQL = "PostgreSQL"
    MYSQL = "MySQL"
    SQLITE = "SQLite"
