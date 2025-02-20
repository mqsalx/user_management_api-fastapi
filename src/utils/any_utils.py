# /src/utils/any_utils.py

from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash


class AnyUtils:

    @staticmethod
    def generate_formatted_datetime() -> str:
        """Generate a formatted timestamp for database storage."""

        now = datetime.now()
        formatted_datetime = now.strftime("%y-%m-%d %H:%M:%S")

        return formatted_datetime

    @staticmethod
    def generate_unique_id() -> str:

        now = datetime.now()
        unique_id = now.strftime("%y%m%d%H%M%S")
        return unique_id

    @staticmethod
    def generate_password_hash(password: str) -> str:
        return generate_password_hash(
            password,
            method="pbkdf2:sha256",
        )

    @staticmethod
    def check_password_hash(
        request_password: str, saved_password: str
    ) -> bool:
        return check_password_hash(saved_password, request_password)
