from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from . import  settings


async def on_startup():
    await Tortoise.init(config=settings.TORTOISE_ORM)


async def on_shutdown():
    await Tortoise.close_connections()


def init_app(main_app: Starlette):
    @main_app.on_event("startup")
    async def startup() -> None:
        await rearq.init()

    @main_app.on_event("shutdown")
    async def shutdown() -> None:
        await rearq.close()


def create_app():
    fast_app = FastAPI(debug=settings.DEBUG)
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fast_app.add_middleware(SentryAsgiMiddleware)

    register_tortoise(fast_app, config=settings.TORTOISE_ORM)
    init_app(fast_app)

    return fast_app
