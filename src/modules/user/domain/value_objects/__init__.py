# /src/modules/user/domain/value_objects__init__.py

from src.modules.user.domain.value_objects.email import Email
from src.modules.user.domain.value_objects.ID import ID
from src.modules.user.domain.value_objects.password import Password
from src.modules.user.domain.value_objects.status import Status

__all__: list[str] = [
    "Email",
    "ID",
    "Password",
    "Status",
]
