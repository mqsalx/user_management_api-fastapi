# /src/utils/auth/__init__.py

# flake8: noqa: E501

# PY
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidKeyError,
    InvalidTokenError,
)
from typing import Any
from werkzeug.security import check_password_hash, generate_password_hash

# Core
from src.core.configurations.environment import EnvConfig
from src.core.configurations.database import DatabaseConfig
from src.core.exceptions import UnauthorizedTokenException


# Utils
from src.utils.logger import log

# Env variables Setup
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = EnvConfig().jwt_access_token_expire_minutes
JWT_SECRET_KEY = EnvConfig().jwt_secret_key
JWT_ALGORITHM = EnvConfig().jwt_algorithm


class AuthUtil:
    """
    Class responsible for handling JSON Web Token (JWT) operations.

    This class provides methods for creating, verifying, and decoding JWT tokens.

    Class Args:
        None
    """

    @staticmethod
    def create_token(
        data: dict,
        expires_delta: timedelta | None = None
    ) -> str:
        """
        Static method responsible for creating a JWT access token.

        This method encodes user-related data into a JWT token with an expiration time.

        Args:
            data (dict): The payload to be encoded in the token.
            expires_delta (timedelta | None, optional): The time until the token expires.
                Defaults to `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`.

        Returns:
            str: The generated JWT token.
        """

        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        expire = now + (
            expires_delta or timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload=to_encode,
            key=JWT_SECRET_KEY,
            algorithm=JWT_ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def verify_token(cls, access_token: str) -> Any:
        """
        Static method responsible for verifying and decoding a JWT token.

        This method decodes a JWT token, ensuring its validity and integrity.

        Args:
            token (str): The JWT token to be verified.

        Returns:
            dict: The decoded token payload.

        Raises:
            UnauthorizedTokenException: If the token is expired, invalid, or has an incorrect signature.
            HTTPException: If an unexpected error occurs during verification.
        """

        try:
            payload: Any = jwt.decode(
                jwt=access_token,
                key=JWT_SECRET_KEY,
                algorithms=JWT_ALGORITHM
            )

            return payload
        except ExpiredSignatureError:
            try:
                payload = jwt.decode(
                    jwt=access_token,
                    key=JWT_SECRET_KEY,
                    algorithms=[JWT_ALGORITHM],
                    options={"verify_exp": False}
                )
                jti = payload.get("jti")
                if jti:
                    cls.validate_session(jti)
                    log.warning(f"Expired token with jti {jti} added to inactive session!")
            except Exception as decode_error:
                log.error(f"Error decoding expired token for blacklist: {decode_error}")
            raise UnauthorizedTokenException("Token expired!")
        except InvalidTokenError:
            raise UnauthorizedTokenException("Invalid token!")
        except InvalidKeyError:
            raise UnauthorizedTokenException("Invalid signing key!")
        except Exception as error:
            log.error(f"Unexpected error in verify_token: {error}")
            raise HTTPException(
                status_code=500,
                detail=f"JWT decoding error: {str(error)}"
            )

    @staticmethod
    def check_password_hash(
        request_password: str, saved_password: str
    ) -> bool:
        """
        Static method responsible for verifying a password.

        This method checks if a provided password matches a stored hashed password.

        Args:
            request_password (str): The plain-text password entered by the user.
            saved_password (str): The hashed password stored in the database.

        Returns:
            bool: True if the passwords match, otherwise False.
        """

        return check_password_hash(saved_password, request_password)

    @staticmethod
    def generate_password_hash(password: str) -> str:
        """
        Static method responsible for hashing a password.

        This method hashes a given password using the PBKDF2-SHA256 algorithm.

        Args:
            password (str): The plain-text password to hash.

        Returns:
            str: The hashed password.
        """

        return generate_password_hash(
            password=password,
            method="pbkdf2:sha256",
        )

    @classmethod
    def validate_session(cls, jti: str) -> None:
        """
        Validates if a session with the given JTI exists and is active.

        Args:
            jti (str): The JWT ID extracted from the token.

        Raises:
            UnauthorizedTokenException: If the session does not exist or is inactive.
        """
        session_db = next(DatabaseConfig().get_db())
        try:
            from src.data.models import SessionAuthModel
            from src.data.repositories import AuthRepository
            __repository = AuthRepository(SessionAuthModel, session_db)
            session = __repository.find_session_by_jti(jti)
            if session or (session.is_active is True):
                update_data = {
                    "is_active": False,
                    "logout_at": datetime.now(),
                }
                __repository.deactivate_session(session, update_data)
        finally:
            session_db.close()