from datetime import datetime, timezone

from sqlmodel import Column, Field, SQLModel
from sqlalchemy.dialects.postgresql import TIMESTAMP


class TimeStampMixin:
    created_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False,
        )
    )
