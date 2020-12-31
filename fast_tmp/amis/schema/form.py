from typing import List

from pydantic import HttpUrl

from . import BaseAmisModel
from .enums import TypeEnum
from .widgets import Control


class Form(BaseAmisModel):
    type = TypeEnum.form
    api: HttpUrl
    controls: List[Control]
