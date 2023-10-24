from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.routes.api import router as api_router
from app.core.config import get_app_settings
from app.core.middlewares import add_custom_middlewares
from app.db.mongo import register_mongodb_to_app
from app.db.redis import register_redis_to_app
from app.services.beanie import init_beanie_user
from app.services.cache import init_redis_cache


def get_application() -> FastAPI:
    settings = get_app_settings()

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    add_custom_middlewares(application, settings)

    register_mongodb_to_app(application, settings)
    register_redis_to_app(application, settings)
    init_redis_cache(application, settings)
    init_beanie_user(application, settings)
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=settings.api_prefix)

    return application


app = get_application()
