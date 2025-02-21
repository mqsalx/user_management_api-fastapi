# /src/utils/jwt_utils.py

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidKeyError,
    InvalidTokenError,
)

from src.core.configurations.env_configuration import EnvConfiguration
from src.core.exceptions.jwt_exception import UnauthorizedToken
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()

# Env variables Setup
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = (
    EnvConfiguration().jwt_access_token_expire_minutes
)
JWT_SECRET_KEY = EnvConfiguration().jwt_secret_key
JWT_ALGORITHM = EnvConfiguration().jwt_algorithm


class JWTUtil:

    @staticmethod
    def create_token(
        data: dict, expires_delta: timedelta | None = None
    ) -> str:
        """
        Creates a JWT access token.
        """

        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Checks and decodes a JWT token.
        """
        try:
            payload = jwt.decode(
                token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
            )
            return payload
        except ExpiredSignatureError:
            raise UnauthorizedToken("Token expired!")
        except InvalidTokenError:
            raise UnauthorizedToken("Invalid token!")
        except InvalidKeyError:
            raise UnauthorizedToken("Invalid signing key!")
        except Exception as e:
            log.error(f"Unexpected error in verify_token: {e}")
            raise HTTPException(
                status_code=500, detail=f"JWT decoding error: {str(e)}"
            )
