# /src/core/exceptions/base/base_exceptions.py


class BaseException(Exception):
    """Base class for all application-specific exceptions."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self):
        """Converts the exception to a dictionary for consistent error responses."""
        return {"detail": self.message}
