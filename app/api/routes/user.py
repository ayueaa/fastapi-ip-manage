
from fastapi import APIRouter, Depends, Query
import motor

from app.api.dependencies.auth import current_superuser
from app.api.models.user import PageUserResponse, User

from app.db.mongo import get_user_coll

router = APIRouter()

# 创建文档


@router.get("/", response_model=PageUserResponse, response_description="获取所有文档")
async def read_documents(
    page: int = Query(1, gt=0, description="页码,从1开始"),
    page_size: int = Query(10, gt=0, lt=50, description="每页大小,1到50之间"),
    user: User = Depends(current_superuser),
    user_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(
        get_user_coll
    ),
):
    skip = (page - 1) * page_size
    total_users = await user_coll.estimated_document_count()  # 获取用户总数
    users = (
        await user_coll.find({})
        .skip(skip)
        .limit(page_size)
        .to_list(page_size)
    )
    for user in users:
        user["id"] = str(user.pop("_id"))
    return PageUserResponse(
        total=total_users, page=page, page_size=page_size, items=users
    )
