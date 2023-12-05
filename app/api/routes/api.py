from fastapi import APIRouter

from app.api.dependencies.auth import auth_backend, fastapi_users
from app.api.models.auth import UserCreate, UserRead, UserUpdate
from app.api.routes import documents, overview, search, user

router = APIRouter()
router.include_router(overview.router, tags=["overview"], prefix="/overview")
router.include_router(search.router, tags=["search"], prefix="/search")
router.include_router(documents.router, tags=["docs"], prefix="/docs")

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
router.include_router(
    user.router,
    prefix="/users",
    tags=["users"],
)
