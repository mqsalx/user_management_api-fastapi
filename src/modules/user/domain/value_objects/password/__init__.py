# /src/modules/user/domain/value_objects/password/__init__.py

from src.shared.utils import AuthUtil


class Password:
    """
    Class representing a Value Object that represents
    and manages a secure user password.

    This class encapsulates the logic for hashing, storing,
        and verifying passwords, ensuring consistent
        and secure handling of user credentials.
    """
    def __init__(self, raw_password: str, already_hashed: bool = False) -> None:
        """
        Constructor method that initializes the Password object,
            optionally hashing the provided password.

        Args:
            raw_password (str): The plaintext or already-hashed password.
            already_hashed (bool): Indicates whether the
                password is already hashed.
                If True, the password will be stored directly without hashing.

        Raises:
            ValueError: If the password is empty or invalid.
        """
        if already_hashed:
            self._value = raw_password
        else:
            self._value = AuthUtil.generate_password_hash(raw_password)

    @property
    def hashed(self) -> str:
        """
        Public method that returns the hashed value of the password.

        Returns:
            str: The hashed password string.
        """
        return self._value

    def check(self, raw_password: str) -> bool:
        """
        Public method that verifies whether the provided raw password matches the stored hash.

        Args:
            raw_password (str): The plaintext password to validate.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return AuthUtil.check_password_hash(raw_password, self._value)
