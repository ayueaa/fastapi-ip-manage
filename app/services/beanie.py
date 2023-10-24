from beanie import init_beanie
from fastapi import FastAPI
from loguru import logger

from app.api.models.user import User
from app.core.settings.app import AppSettings


def init_beanie_user(app: FastAPI, app_settings: AppSettings):
    @app.on_event("startup")
    async def init_beanie_user():
        await init_beanie(
            database=app.state.mongo_client[app_settings.db], document_models=[User]
        )
        logger.info("init beanie user.")
