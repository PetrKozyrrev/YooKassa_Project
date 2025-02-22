from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aerich import Command
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import RegisterTortoise

from .clients import TORTOISE_ORM
from .routes import backend_router, frontend_router
from .schedules import start_scheduler

origins = [
    "*",
]


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
    aerich = Command(tortoise_config=TORTOISE_ORM)

    await aerich.init()
    await aerich.upgrade()
    start_scheduler()
    async with RegisterTortoise(
        app=fastapi_app,
        config=TORTOISE_ORM,
    ):
        yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(backend_router)
app.include_router(frontend_router)
