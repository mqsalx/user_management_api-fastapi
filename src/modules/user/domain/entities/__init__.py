# /src/modules/user/domain/entities/__init__.py

# PY
from datetime import datetime

# Shared
from src.shared.domain.entities.base import BaseEntity


class UserEntity(BaseEntity):
    """
    Domain entity representing a user within the system.

    This class encapsulates user-related attributes
        and inherits base properties
    such as `entity_id`, `created_at`, and `updated_at` from `BaseEntity`.

    Class Args:
        name (str): The user's name.
        email (str): The user's email.
        password (str): The user's password (should be hashed).
        status (str): The user's status (e.g., 'active').
        user_id (str | None): Optional UUID for the user.
            Auto-generated if not provided.
        role_id (str | None): Optional role ID associated with the user.
        created_at (datetime | None): Creation timestamp.
        updated_at (datetime | None): Last update timestamp.
    """

    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        status: str,
        user_id: str | None = None,
        role_id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        """
        Initializes a new UserEntity instance.

        Args:
            name (str): The user's name.
            email (str): The user's email.
            password (str): The user's password (should be hashed).
            status (str): The user's status (e.g., 'active').
            user_id (str | None): Optional UUID for the user.
                Auto-generated if not provided.
            role_id (str | None): Optional role ID associated with the user.
            created_at (datetime | None): Creation timestamp.
            updated_at (datetime | None): Last update timestamp.
        """
        super().__init__(
            entity_id=user_id, created_at=created_at, updated_at=updated_at
        )
        self._name = name
        self._email = email
        self._password = password
        self._status = status
        self._user_id: str | None = user_id
        self._role_id: str | None = role_id

    @property
    def user_id(self) -> str | None:
        """
        Returns the user ID.

        Returns:
            str | None: The UUID of the user.
        """
        return self._user_id

    @property
    def name(self) -> str:
        """
        Returns the user's name.

        Returns:
            str: The full name of the user.
        """
        return self._name

    @property
    def email(self) -> str:
        """
        Returns the user's email.

        Returns:
            str: The email address of the user.
        """
        return self._email

    @property
    def password(self) -> str:
        """
        Returns the user's hashed password.

        Returns:
            str: The password hash.
        """
        return self._password

    @property
    def status(self) -> str:
        """
        Returns the user's status.

        Returns:
            str: The current status of the user (e.g., 'active', 'inactive').
        """
        return self._status

    @property
    def role_id(self) -> str | None:
        """
        Returns the role ID associated with the user.

        Returns:
            str | None: The role identifier or None if not assigned.
        """
        return self._role_id
