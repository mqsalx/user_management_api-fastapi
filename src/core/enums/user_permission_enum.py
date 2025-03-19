# /src/core/enums/user_permission_enum.py

from enum import Enum


class UserPermissionEnum(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
