from fastapi import APIRouter, Depends

from app.api.users.user_manager import (
    auth_backend,
    fastapi_users,
    google_oauth_client,
    current_active_user,
)
from app.api.users.schemas import UserCreate, UserRead, UserUpdate
from app.api.users.models import User


from app.core.config import settings

users = APIRouter()

users.include_router(
    fastapi_users.get_auth_router(
        auth_backend,
        requires_verification=True,
    ),
    prefix="/auth/jwt",
    tags=["auth"],
)

users.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

users.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

users.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

users.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True),
    prefix="/users",
    tags=["users"],
)

users.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client, auth_backend, settings.SECRET, associate_by_email=True
    ),
    prefix="/auth/google",
    tags=["auth"],
)

users.include_router(
    fastapi_users.get_oauth_associate_router(google_oauth_client, UserRead, "SECRET"),
    prefix="/auth/associate/google",
    tags=["auth"],
)


@users.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
