# /src/modules/user/presentation/schemas/__init__.py

# Request
from src.modules.user.presentation.schemas.request.body import (
    CreateUserReqBodyReq,
    UpdateUserReqBodyReq,
)
from src.modules.user.presentation.schemas.request.path import (
    FindUserByUserIdPathReq,
    RemoveUserByUserIdReqPathReq,
    UpdateUserReqPathReq,
)
from src.modules.user.presentation.schemas.request.query import (
    FindAllUsersQueryReq,
    FindUserByUserIdQueryReq,
)

# Response
from src.modules.user.presentation.schemas.response.create import (
    CreateUserResponse,
)
from src.modules.user.presentation.schemas.response.find.all import (
    FindAllUsersResponse,
)
from src.modules.user.presentation.schemas.response.find.by_user_id import (
    FindUserByUserIdResponse,
)
from src.modules.user.presentation.schemas.response.update import (
    UpdateUserResponse,
)

__all__: list[str] = [
    "CreateUserReqBodyReq",
    "CreateUserResponse",
    "UpdateUserReqBodyReq",
    "FindAllUsersQueryReq",
    "FindUserByUserIdPathReq",
    "FindUserByUserIdQueryReq",
    "FindAllUsersResponse",
    "FindUserByUserIdResponse",
    "RemoveUserByUserIdReqPathReq",
    "UpdateUserReqPathReq",
    "UpdateUserResponse",
]
