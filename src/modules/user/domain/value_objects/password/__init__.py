# /src/modules/user/domain/value_objects/password/__init__.py

from src.utils import AuthUtil


class Password:
    def __init__(self, raw_password: str, already_hashed: bool = False):
        if already_hashed:
            self._value = raw_password
        else:
            self._value = AuthUtil.generate_password_hash(raw_password)

    @property
    def hashed(self) -> str:
        return self._value

    def check(self, raw_password: str) -> bool:
        return AuthUtil.verify_password(raw_password, self._value)
