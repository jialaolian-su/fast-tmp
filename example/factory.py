# -*- encoding: utf-8 -*-
"""
@File    : factory.py
@Time    : 2020/12/2 21:57
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from . import settings


async def init_app(app: Starlette):
    @app.on_event("startup")
    async def startup():
        """
        在项目开始的时候，把所有的异步服务启动起来,包括orm服务，redis服务，cache与消息队列服务等
        异步服务需要提前启动，把需要的服务加到异步循环里面
        """
        await Tortoise.init(config=settings.TORTOISE_ORM)

    @app.on_event("shutdown")
    async def shutdown():
        """
        项目结束的时候关闭启动的服务
        :return:
        """
        await Tortoise.close_connections()


def create_app():
    fast_app = FastAPI(debug=settings.DEBUG)
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许的域
        allow_credentials=True,  # 指跨域的时候允许cookie
        allow_methods=["*"],  # 允许的http方法，(get,post,put等)
        allow_headers=["*"],  # 允许特定的标头，如果为*则所有的都可以
    )
    fast_app.add_middleware(SentryAsgiMiddleware)
    register_tortoise(fast_app, config=settings.TORTOISE_ORM)
    init_app(fast_app)

    return fast_app
