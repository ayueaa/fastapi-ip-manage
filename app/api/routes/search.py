import motor.motor_asyncio
from fastapi import APIRouter, Depends

from app.api.dependencies.auth import current_active_user
from app.api.errors.http_error import NotFound404Error
from app.api.models.search import SearchItem, SearchResponse
from app.api.models.user import User
from app.db.mongo import get_history_coll, get_visable_coll

router = APIRouter()


@router.post("/ip/", response_model=SearchResponse, response_description="ip情报查询")
async def ip_search(
    ip_query: SearchItem,
    history_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(
        get_history_coll
    ),
    visable_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(
        get_visable_coll
    ),
    user: User = Depends(current_active_user),
):
    ip = str(ip_query.ip)

    ip_visable_doc = await visable_coll.find_one({"ip": ip})
    if not ip_visable_doc:
        raise NotFound404Error()
    # 返回最多10条历史记录
    ip_history_docs = (
        await history_coll.find({"ip": ip}).sort([("last_seen", -1)]).to_list(10)
    )
    ip_history_docs.sort(key=lambda x: x["last_seen"], reverse=True)
    return SearchResponse(visable=ip_visable_doc, history=ip_history_docs)
