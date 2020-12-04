# -*- encoding: utf-8 -*-
"""
@File    : app.py
@Time    : 2020/12/2 22:57
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import json
import logging
import typing

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_422_UNPROCESSABLE_ENTITY

from example import settings

from example.errors import Forbidden, TokenInvalid, UnKnownError, UserBaned
from example.exceptions import ErrorException, UserBanedError
# from .routes import api_router, notify_router, yl_notify_router
from .views import router

logger = logging.getLogger("example.app1")


async def error_exception_handler(request: Request, exc: ErrorException):
    if isinstance(exc, UserBanedError):
        ret = UserBaned().dict()
        if settings.DEBUG:
            return ORJSONResponse(ret)
        return AesResponse(ret)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    detial = exc.detail
    if exc.status_code == HTTP_401_UNAUTHORIZED:
        ret = TokenInvalid(msg=exc.detail).dict()
    elif exc.status_code == HTTP_403_FORBIDDEN:
        ret = Forbidden(msg=exc.detail).dict()
    else:
        logger.error(f"HTTPException: {exc.detail}", exc_info=True)
        ret = UnKnownError(msg=exc.detail).dict()
    if settings.DEBUG:
        return JSONResponse(ret)
    return AesResponse(ret)


async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    捕捉422报错并进行自定义处理
    :param request:
    :param exc:
    :return:
    """
    x = exc.errors()
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": jsonable_encoder(exc.errors())},
    )


class AesResponse(PlainTextResponse):
    def render(self, content: typing.Any) -> bytes:
        """
        返回类，可以在这里进行返回数据全局加密等
        :param content:
        :return:
        """
        content = json.dumps(content)
        self.media_type = "application/json"
        return super(AesResponse, self).render(content)


app = FastAPI(
    title="app1的接口文档",
    debug=settings.DEBUG,
    default_response_class=AesResponse,  # 自定义返回类
)

app.add_exception_handler(ErrorException, error_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.include_router(router=router, prefix="/app1")
app.openapi()
# app.include_router(notify_router)
# app.include_router(yl_notify_router)
