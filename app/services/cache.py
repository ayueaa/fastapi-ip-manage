from fastapi import FastAPI
from loguru import logger
from app.core.settings.app import AppSettings

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


def init_redis_cache(app: FastAPI, app_settings: AppSettings):
    @app.on_event("startup")
    def init_redis_cache():
        FastAPICache.init(RedisBackend(app.state.redis_cli), prefix="fastapi-cache")
        logger.info("init redis cache.")
