from datetime import datetime, timedelta
from typing import Dict, List

import motor.motor_asyncio
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
import psutil

from app.api.dependencies.auth import current_active_user
from app.api.models.overview import CountGroupResponse, OverviewResponse
from app.api.models.user import User
from app.api.utils import agg_recent_days_count
from app.db.mongo import get_history_coll, get_visable_coll

router = APIRouter()


@router.get("/history", response_model=OverviewResponse, response_description="历史数据量概览")
@cache(expire=60 * 10)
async def overview_hiostory(
    history_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(
        get_history_coll
    ),
    user: User = Depends(current_active_user),
):
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


@router.get(
    "/group/source", response_model=Dict[str, int], response_description="数据源聚合数"
)
@cache(expire=60 * 10)
async def overview_group(
    history_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(
        get_history_coll
    ),
    user: User = Depends(current_active_user),
):
    pipeline = [
        {"$group": {"_id": "$source", "count": {"$sum": 1}}},
        {"$project": {"source": "$_id", "count": 1, "_id": 0}},
    ]
    result = await history_coll.aggregate(pipeline).to_list(None)
    return {doc["source"]: doc["count"] for doc in result}


@router.get("/group/tag", response_model=Dict[str, int], response_description="tag聚合")
@cache(expire=60 * 10)
async def overview_tag(
    history_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(
        get_history_coll
    ),
    user: User = Depends(current_active_user),
):
    pipeline = [
        {"$unwind": "$raw_tags"},
        {"$group": {"_id": "$raw_tags", "count": {"$sum": 1}}},
        {"$project": {"tag": "$_id", "count": 1, "_id": 0}},
    ]
    result = await history_coll.aggregate(pipeline).to_list(None)
    return {doc["tag"]: doc["count"] for doc in result}


@router.get(
    "/7daycount/history",
    response_model=List[CountGroupResponse],
    response_description="最近七日历史情报更新数量",
)
@cache(expire=60 * 10)
async def overview_7_days_history_count(
    history_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(
        get_history_coll
    ),
    user: User = Depends(current_active_user),
):
    results = await agg_recent_days_count(recent_days=7, coll=history_coll)
    return results


@router.get(
    "/7daycount/visable",
    response_model=List[CountGroupResponse],
    response_description="最近七日唯一IP情报更新数量",
)
@cache(expire=60 * 10)
async def overview_7_days_visable_count(
    visable_coll: motor.motor_asyncio.AsyncIOMotorCollection = Depends(
        get_visable_coll
    ),
    user: User = Depends(current_active_user),
):
    results = await agg_recent_days_count(recent_days=7, coll=visable_coll)
    return results


@router.get("/system-info")
@cache(expire=60 * 1)
async def get_system_info():
    system_info = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory()._asdict(),
        "disk_usage": psutil.disk_usage('/')._asdict(),
        "network_stats": psutil.net_io_counters()._asdict()
    }
    return system_info
