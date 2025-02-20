# /src/utils/jwt_utils.py

from datetime import datetime, timedelta, timezone

import jwt

from src.core.configurations.env_configuration import EnvConfiguration

# Env variables Setup
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = (
    EnvConfiguration().jwt_access_token_expire_minutes
)
JWT_SECRET_KEY = EnvConfiguration().jwt_secret_key
JWT_ALGORITHM = EnvConfiguration().jwt_algorithm


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
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


def verify_token(token: str) -> dict:
    """
    Checks and decodes a JWT token.
    """

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Expired token!")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token!")
