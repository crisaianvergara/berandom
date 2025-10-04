import uuid
from datetime import datetime

from sqlmodel import SQLModel

from app.api.rooms.models import RoomBase


class RoomCreate(RoomBase):
    created_at: datetime
    updated_at: datetime


class RoomUpdate(SQLModel):
    room_name: str | None = None


class RoomPublic(RoomBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
