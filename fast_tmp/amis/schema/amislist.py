from pydantic.main import BaseModel

from . import TypeEnum
from .crud import CRUD


class AmisList(BaseModel):
    type = TypeEnum.page
    body: CRUD
