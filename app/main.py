from fastapi import FastAPI

from app.api.router import api_router
from app.api.exception_handlers import register_exception_handlers
from app.core.config import settings
from app.core.logging_config import setup_logging


setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
)

register_exception_handlers(app)
app.include_router(api_router)