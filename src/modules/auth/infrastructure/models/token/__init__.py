# /src/data/models/auth/session/__init__.py

# flake8: noqa: E501

# PY
import uuid

from sqlalchemy import (
    Column,

    String
)
from sqlalchemy.orm import relationship

# Shared
from src.shared.infrastructure.models.base import BaseModel


class TokenModel(BaseModel):
    """
    Class responsible for defining the database model for tokens JWT.

    This model represents the `tokens` table
        and manages tokens-related
        relationships and data operations.

    Class Args:
        None
    """
    token_id: Column[str] = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
        unique=True
    )

    access_token: Column[str] = Column(
        String,
        nullable=False,
        unique=False
    )

    sessions = relationship(
        argument="SessionModel",
        back_populates="tokens",
        cascade="all, delete-orphan"
    )
