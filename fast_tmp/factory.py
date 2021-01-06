import os
import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fast_tmp.api.auth import auth_router
from fast_tmp.api.auth2 import auth2_router
from fast_tmp.conf import settings

paths = sys.path


def get_dir():
    return os.path.dirname(__file__)


DIR = get_dir()


def create_fast_tmp_app():
    fast_tmp_app = FastAPI(debug=settings.DEBUG)
    if settings.DEBUG:
        fast_tmp_app.mount(
            "/static", StaticFiles(directory=os.path.join(DIR, "static")), name="static"
        )
    else:
        fast_tmp_app.mount(
            "/static",
            StaticFiles(directory=os.path.join(settings.BASE_DIR, settings.STATIC_ROOT)),
            name="static",
        )
    fast_tmp_app.include_router(auth_router)
    fast_tmp_app.include_router(auth2_router)
    # fast_tmp_app.add_exception_handler(
    #     HTTPException, http_exception_handler
    # )
    # fast_tmp_app.add_exception_handler(
    #     ErrorException, error_exception_handler
    # )
    # fast_tmp_app.add_exception_handler(
    #     RequestValidationError, validation_exception_handler
    # )
    return fast_tmp_app
