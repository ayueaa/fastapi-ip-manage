from fastapi import APIRouter

from app.api.routes import comments

router = APIRouter()
router.include_router(comments.router, tags=["comments"], prefix="/articles")
