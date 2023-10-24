from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.settings.app import AppSettings


def add_custom_middlewares(app: FastAPI, app_settings: AppSettings):
    @app.middleware("http")
    async def system_error_handle(request: Request, call_next) -> Response:
        logger.info("...middleware..")
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(e)
            return JSONResponse({"errors": "系统错误,请联系管理员"}, status_code=500)
        return response
