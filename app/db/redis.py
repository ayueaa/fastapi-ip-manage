from fastapi import FastAPI
from loguru import logger
from starlette.requests import Request
from app.core.settings.app import AppSettings

from redis import asyncio as aioredis


def register_redis_to_app(app: FastAPI, app_settings: AppSettings):
    @app.on_event("startup")
    async def connect_redis():
        redis_cli = await aioredis.from_url(app_settings.redis_url)
        app.state.redis_cli = redis_cli
        logger.info("Connected to redis.")
        return redis_cli

    @app.on_event("shutdown")
    async def close_redis():
        if hasattr(app.state.redis_cli, "close"):
            await app.state.redis_cli.close()
            logger.info("Disconnected redis.")


async def get_redis_conn(request: Request) -> aioredis.client.Redis:
    return request.app.state.redis_cli
