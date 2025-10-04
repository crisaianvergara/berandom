from fastapi import APIRouter, Depends, HTTPException, status, Query

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession as Session

from app.api.rooms.models import Room
from app.api.rooms.schemas import RoomCreate, RoomPublic, RoomUpdate
from app.api.users.models import User
from app.api.users.user_manager import current_active_user
from app.core.db import get_async_session

rooms = APIRouter(prefix="/rooms", tags=["rooms"])


@rooms.post("/", status_code=status.HTTP_201_CREATED, response_model=RoomPublic)
async def create_room(
    *,
    session: Session = Depends(get_async_session),
    room: RoomCreate,
    user: User = Depends(current_active_user)
) -> RoomPublic:
    db_room = Room.model_validate(room)
    session.add(db_room)
    await session.commit()
    await session.refresh(db_room)
    return db_room


@rooms.get("/{room_id}", response_model=RoomPublic)
async def read_room(
    *,
    session: Session = Depends(get_async_session),
    room_id: str,
    user: User = Depends(current_active_user)
) -> RoomPublic:
    room = await session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found.")
    return room


@rooms.get("/", response_model=list[RoomPublic])
async def read_rooms(
    *,
    session: Session = Depends(get_async_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    user: User = Depends(current_active_user)
) -> list[RoomPublic]:
    rooms = await session.exec(select(Room).offset(offset).limit(limit))

    return rooms.all()


@rooms.patch("/{room_id}", response_model=RoomPublic)
async def update_room(
    *,
    session: Session = Depends(get_async_session),
    room_id: str,
    room: RoomUpdate,
    user: User = Depends(current_active_user)
) -> RoomPublic:
    db_room = await session.get(Room, room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found.")

    room_data = room.model_dump(exclude_unset=True)
    db_room.sqlmodel_update(room_data)
    session.add(db_room)
    await session.commit()
    await session.refresh(db_room)
    return db_room


@rooms.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    *,
    session: Session = Depends(get_async_session),
    room_id: str,
    user: User = Depends(current_active_user)
):
    room = await session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found.")
    await session.delete(room)
    await session.commit()
    return {}
