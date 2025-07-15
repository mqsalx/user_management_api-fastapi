# /src/modules/user/domain/services/__init__.py

from src import utils


class UserService:
    """
    """
    def hash_password(self, password: str) -> str:
        """
        """
        return utils.AuthUtil.generate_password_hash(password=password)
