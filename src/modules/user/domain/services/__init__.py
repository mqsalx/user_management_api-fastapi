# /src/modules/user/domain/services/__init__.py

from src import utils


class UserService:
    """
    Class representing the service layer responsible
        for user-related domain logic.

    This class provides helper methods that encapsulate operations such as
    password hashing, which are used during user creation or updates.
    """

    def hash_password(self, password: str) -> str:
        """
        Public method that hashes a plain-text password using
            the application's configured algorithm.

        Args:
            password (str): The plain-text password to be hashed.

        Returns:
            str: The securely hashed password.
        """
        return utils.AuthUtil.generate_password_hash(password=password)
