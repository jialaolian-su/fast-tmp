from typing import List, Union

from fast_tmp.amis.schema.abstract_schema import BaseAmisModel

from .enums import TypeEnum


class Page(BaseAmisModel):
    type = TypeEnum.page
    body: Union[BaseAmisModel, List[BaseAmisModel]]
