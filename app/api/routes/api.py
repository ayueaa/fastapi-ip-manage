from fastapi import APIRouter

from app.api.routes import overview

router = APIRouter()
router.include_router(overview.router, tags=["overview"], prefix="/overview")
