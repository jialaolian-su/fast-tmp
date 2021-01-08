from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from fast_tmp.conf import settings
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def init_app(main_app: FastAPI):
    @main_app.on_event("startup")
    async def startup() -> None:
        pass

    @main_app.on_event("shutdown")
    async def shutdown() -> None:
        pass


def create_app():
    app = FastAPI(debug=settings.DEBUG)
    # app.mount(settings.ADMIN_URL, r_app)
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
