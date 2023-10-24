from datetime import datetime, timedelta

import motor.motor_asyncio
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.api.dependencies.auth import current_active_user, current_superuser
from app.api.models.overview import OverviewResponse
from app.api.models.user import User
from app.db.mongo import get_history_coll, get_visable_coll

router = APIRouter()


@router.get("/history", response_model=OverviewResponse, response_description="历史数据量概览")
@cache(expire=60 * 10)
async def overview_hiostory(
    history_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(
        get_history_coll
    ),
    user: User = Depends(current_superuser),
):
    print(user.email)
    now = datetime.now()
    today_midnight = datetime(now.year, now.month, now.day)
    last_7day_midnight = today_midnight - timedelta(days=7)

    total = await history_coll.estimated_document_count()
    increase_today = await history_coll.count_documents(
        {"last_seen": {"$gt": int(today_midnight.timestamp())}}
    )
    increase_7days = await history_coll.count_documents(
        {"last_seen": {"$gt": int(last_7day_midnight.timestamp())}}
    )
    return OverviewResponse(
        total=total, increase_today=increase_today, increase_7day=increase_7days
    )


@router.get(
    "/visable", response_model=OverviewResponse, response_description="唯一IP数据量概览"
)
@cache(expire=60 * 10)
async def overview_visable(
    visable_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(
        get_visable_coll
    ),
    user: User = Depends(current_active_user),
):
    now = datetime.now()
    today_midnight = datetime(now.year, now.month, now.day)
    last_7day_midnight = today_midnight - timedelta(days=7)

    total = await visable_coll.estimated_document_count()
    increase_today = await visable_coll.count_documents(
        {"last_seen": {"$gt": int(today_midnight.timestamp())}}
    )
    increase_7days = await visable_coll.count_documents(
        {"last_seen": {"$gt": int(last_7day_midnight.timestamp())}}
    )
    return OverviewResponse(
        total=total, increase_today=increase_today, increase_7day=increase_7days
    )
