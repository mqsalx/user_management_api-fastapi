# /src/core/enums/user_role_enum.py

from enum import Enum


class UserRoleEnum(str, Enum):

    SUPER_ADMINISTRATOR = "super_administrator"
    ADMINISTRATOR = "administrator"
    DEFAULT = "default"
