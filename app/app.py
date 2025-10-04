from fastapi import FastAPI

from app.core.config import settings
from app.api.rooms.routes import rooms
from app.api.users.routes import users

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Fastapi templates",
)

app.include_router(users)
app.include_router(rooms)
