from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.applications import Starlette

from example import rearq
from fast_tmp.amis_app import AmisAPI
from fast_tmp.conf import settings
from starlette.middleware.cors import CORSMiddleware
from fast_tmp import factory
from tortoise import Tortoise

from fast_tmp.redis import AsyncRedisUtil


@rearq.on_startup
async def on_startup():
    await AsyncRedisUtil.init(**settings.REDIS)
    await Tortoise.init(config=settings.TORTOISE_ORM)


@rearq.on_shutdown
async def on_shutdown():
    await AsyncRedisUtil.close()
    await Tortoise.close_connections()


def init_app(main_app: Starlette):
    @main_app.on_event("startup")
    async def startup() -> None:
        await AsyncRedisUtil.init(**settings.REDIS)
        await Tortoise.init(config=settings.TORTOISE_ORM)
        await rearq.init()

    @main_app.on_event("shutdown")
    async def shutdown() -> None:
        await AsyncRedisUtil.close()
        await Tortoise.close_connections()
        await rearq.close()


def create_app() -> AmisAPI:
    app = AmisAPI(title='fast_tmp example',debug=settings.DEBUG)
    r_app = factory.create_fast_tmp_app()
    app.mount(settings.FAST_TMP_URL, r_app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Sentry的插件
    app.add_middleware(SentryAsgiMiddleware)
    init_app(app)
    return app
