import motor.motor_asyncio
from fastapi import FastAPI
from loguru import logger
from starlette.requests import Request

from app.core.config import get_app_settings
from app.core.settings.app import AppSettings


def register_mongodb_to_app(app: FastAPI, app_settings: AppSettings):
    @app.on_event("startup")
    async def connect_mongodb():
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
            app_settings.database_url, maxPoolSize=20
        )
        app.state.mongo_client = mongo_client
        logger.info("Connected to mongodb.")
        return mongo_client

    @app.on_event("shutdown")
    async def close_mongodb():
        if hasattr(app.state.mongo_client, "close"):
            app.state.mongo_client.close()
            logger.info("Disconnected mongodb.")


async def get_history_coll(request: Request):
    settings = get_app_settings()
    return request.app.state.mongo_client[settings.db][settings.history_collection]


async def get_visable_coll(request: Request):
    settings = get_app_settings()
    return request.app.state.mongo_client[settings.db][settings.visable_collection]


async def get_docs_coll(request: Request):
    settings = get_app_settings()
    return request.app.state.mongo_client[settings.db][settings.docs_collection]
