from typing import Any

from pydantic.main import BaseModel


class DefaultRes(BaseModel):
    status: int


class ListOk(DefaultRes):
    status = 0
    msg = ""
    data: Any
