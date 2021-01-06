from typing import List, Union

from fast_tmp.amis.schema.abstract_schema import BaseAmisModel

from .enums import TypeEnum


class Page(BaseAmisModel):
    type = TypeEnum.page
    body: Union[BaseAmisModel, List[BaseAmisModel]]


class HBox(BaseAmisModel):
    type = TypeEnum.hbox
    className: str = "b-a bg-dark lter"
    columns: List[BaseAmisModel]
