import datetime
from loguru import logger
import motor.motor_asyncio
from fastapi import APIRouter, Depends

from app.api.dependencies.auth import current_active_user
from app.api.errors.http_error import NotFound404Error
from app.api.models.search import SearchItem, SearchResponse
from app.api.models.user import User
from app.api.utils import get_ip_info
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
    # user: User = Depends(current_active_user),
):
    ip = str(ip_query.ip)

    ip_visable_doc = await visable_coll.find_one({"ip": ip})
    if not ip_visable_doc:
        raise NotFound404Error()
    # 返回最多10条历史记录
    ip_history_docs = (
        await history_coll.find({"ip": ip}).sort([("last_seen", -1)]).to_list(10)
    )
    logger.info(ip_history_docs)
    for doc in ip_history_docs:
        if isinstance(doc["last_seen"], str):
            doc["last_seen"] = int(datetime.datetime.strptime(
                doc["last_seen"], "%Y-%m-%d %H:%M:%S").timestamp())
    ip_history_docs.sort(key=lambda x: x["last_seen"], reverse=True)

    # token = "deadebdd406657"
    extro_info = get_ip_info(ip) or {}
    return SearchResponse(
        visable=ip_visable_doc, history=ip_history_docs, extro=extro_info)
