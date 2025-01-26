# /src/core/exceptions/base/base_exception.py


class BaseException(Exception):
    """Base class for all application-specific exceptions."""

    def __init__(self, message: str, status_code: int = 400):
        self.__message = message
        self.__status_code = status_code
        super().__init__(message)

    @property
    def status_code(self):
        return self.__status_code

    @property
    def message(self):
        return self.__message

    def to_dict(self):
        """Converts the exception to a dictionary for consistent error responses."""
        return {"detail": self.__message}
