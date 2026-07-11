from fastapi import FastAPI
from app.api.v1.chat import router as chat_router
from app.api.v1.documents import router as document_router
from app.api.v1.health import router as health_router
from app.config.settings import settings

from app.api.v1.auth import router as auth_router

from app.api.v1.study import router as study_router

from app.database.init_db import init_db

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

init_db()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(
    chat_router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    auth_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    document_router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    study_router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    health_router,
    prefix=settings.API_V1_PREFIX
)