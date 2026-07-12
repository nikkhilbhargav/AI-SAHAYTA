from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


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