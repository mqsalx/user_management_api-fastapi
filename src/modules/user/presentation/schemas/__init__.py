# /src/api/schemas/__init__.py

# Request
from src.modules.user.presentation.schemas.request.body import (
    CreateUserReq,
    UpdateUserReq,
)
from src.modules.user.presentation.schemas.request.path import (
    FindUserByUserIdReq,
    RemoveUserReq,
)
from src.modules.user.presentation.schemas.request.query import (
    FindAllUsersReq,
    # FindUserByUserIdReq,
)

# Response
from src.modules.user.presentation.schemas.response import UserResponse

__all__: list[str] = [
    "CreateUserReq",
    "UpdateUserReq",
    "FindAllUsersReq",
    "FindUserByUserIdReq",
    "RemoveUserReq",
    "UserResponse"
]
