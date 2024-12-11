# /app/exceptions/usecases/user/user_exceptions.py

from src.core.exceptions.base.base_exceptions import BaseApplicationException


class UserNotFoundException(BaseApplicationException):
    """Raised when a user is not found in the database."""

    def __init__(self, user_id: int):
        super().__init__(f"User with ID {user_id} not found.", status_code=404)


class EmailAlreadyExistsException(BaseApplicationException):
    """Raised when a user tries to create an account with an existing email."""

    def __init__(self, email: str):
        super().__init__(f"The email '{email}' is already registered.")
