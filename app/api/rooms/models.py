import uuid

from sqlmodel import Field, SQLModel

from app.api.common.mixins import TimeStampMixin


class RoomBase(SQLModel):
    room_name: str = Field(index=True, nullable=False)


class Room(RoomBase, TimeStampMixin, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
