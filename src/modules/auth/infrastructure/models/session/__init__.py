# /src/data/models/auth/session/__init__.py

# PY
import uuid

from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Shared
from src.shared.infrastructure.models.base import BaseModel


class SessionModel(BaseModel):
    """
    Class responsible for defining the database
        model for login sessions.

    This model represents the `sessions` table
        and manages session-related
        relationships and data operations.

    Class Args:
        None
    """
    session_id: Column[str] = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
        unique=True
    )

    token_id: Column[str] = Column(
        String,
        ForeignKey("tokens.token_id"),
        nullable=False
    )

    user_id: Column[str] = Column(
        String,
        ForeignKey(column="users.user_id"),
        nullable=False
    )

    login_at: Column[datetime] = Column(
        DateTime,
        default=func.now(),
        nullable=True
    )

    logout_at: Column[datetime] = Column(
        DateTime,
        nullable=True
    )

    tokens = relationship(
        argument="TokenModel",
        back_populates="sessions"
    )

    users = relationship(
        argument="UserModel",
        back_populates="sessions"
    )
