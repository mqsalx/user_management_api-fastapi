# /src/modules/user/application/dtos/__init__.py

# Input
from src.modules.user.application.dtos.input.create import CreateUserInput
from src.modules.user.application.dtos.input.find.all import FindAllUsersInput
from src.modules.user.application.dtos.input.find.by_user_id import (
    FindUserByUserIdInput,
)
from src.modules.user.application.dtos.input.remove import RemoveUserInput
from src.modules.user.application.dtos.input.update import UpdateUserInput

# Output
from src.modules.user.application.dtos.output.create import CreateUserOutput
from src.modules.user.application.dtos.output.find.all import (
    FindAllUsersOutput,
)
from src.modules.user.application.dtos.output.find.by_user_id import (
    FindUserByUserIdOutput,
)
from src.modules.user.application.dtos.output.update import UpdateUserOutput

__all__: list[str] = [
    "CreateUserInput",
    "CreateUserOutput",
    "FindAllUsersInput",
    "FindUserByUserIdInput",
    "RemoveUserInput",
    "UpdateUserInput",
    "FindAllUsersOutput",
    "FindUserByUserIdOutput",
    "UpdateUserOutput",
]
