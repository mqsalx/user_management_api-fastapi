# /src/data/models/__init__.py

# flake8: noqa: E501, F401

from src.data.models.permission import (
    Base,
    PermissionModel
)
from src.data.models.role import (
    Base,
    RoleModel
)
from src.data.models.role_permission import Base
from src.data.models.user import (
    Base,
    UserModel
)