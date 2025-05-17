# /src/domain/enums/user/__init__.py

# flake8: noqa: E501

from enum import Enum


class UserPermissionEnum(str, Enum):
    """
    Enumerated class for user permissions.

    This enum defines the possible actions that a user can perform in the system.

    Class Args:
        None

    Members:
        CREATE (str): Permission to create new resources.
        READ (str): Permission to read/view existing resources.
        UPDATE (str): Permission to update or modify resources.
        DELETE (str): Permission to delete resources.
    """

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"


class UserRoleEnum(str, Enum):
    """
    Enumerated class for user roles.

    This enum defines the different user roles available in the system.

    Class Args:
        None

    Members:
        SUPER_ADMINISTRATOR (str): Represents a super administrator with the highest level of access.
        ADMINISTRATOR (str): Represents an administrator with elevated privileges.
        DEFAULT (str): Represents a standard user with basic access rights.
    """

    SUPER_ADMINISTRATOR = "super_administrator"
    ADMINISTRATOR = "administrator"
    DEFAULT = "default"


class UserStatusEnum(str, Enum):
    """
    Enumerated class for user account status.

    This enum defines the possible states of a user account in the system.

    Class Args:
        None

    Members:
        ACTIVE (str): Represents an active user with full access.
        INACTIVE (str): Represents a user who has been deactivated and cannot access the system.
        SUSPENDED (str): Represents a user temporarily suspended due to policy violations or other reasons.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"