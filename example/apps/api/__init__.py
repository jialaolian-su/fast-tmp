import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from fast_tmp.conf import settings
from src.apps.api.errors import Forbidden, TokenInvalid, UnKnownError
from src.common import get_docs_description

logger = logging.getLogger("src.api")


async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == HTTP_401_UNAUTHORIZED:
        ret = TokenInvalid(msg=exc.detail).dict()
    elif exc.status_code == HTTP_403_FORBIDDEN:
        ret = Forbidden(msg=exc.detail).dict()
    else:
        logger.error(f"HTTPException: {exc.detail}", exc_info=True)
        ret = UnKnownError(msg=exc.detail).dict()
    return ORJSONResponse(ret)


app = FastAPI(
    title="真人平台API接口文档",
    debug=settings.DEBUG,
    description=get_docs_description(),
)

app.add_exception_handler(HTTPException, http_exception_handler)
