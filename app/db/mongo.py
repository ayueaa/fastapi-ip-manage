from ctypes import Union

import motor.motor_asyncio
from fastapi import FastAPI
from loguru import logger

from app.core.settings.app import AppSettings

mongo_client: motor.motor_asyncio.AsyncIOMotorClient = None


def register_mongodb_to_app(app: FastAPI, app_settings: AppSettings):
    @app.on_event("startup")
    async def connect_mongodb():
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
            app_settings.database_url, maxPoolSize=20)
        app.state.mongo_client = mongo_client
        logger.info("Connected to mongodb.")
        return mongo_client

    @app.on_event("shutdown")
    async def close_mongodb():
        if hasattr(mongo_client, "close"):
            mongo_client.close()
            logger.info("Disconnected mongodb.")
