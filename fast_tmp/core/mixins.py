from typing import List, Dict, Type, Any, Callable, Iterable, Tuple
from enum import Enum
from pydantic import BaseModel
from pydantic.utils import get_model
from tortoise import Model
from fastapi import APIRouter, Depends
from .choices import Method, ViewType
from .filter import search_depend
from ..utils.model import get_model_from_str


class RequestMixin(BaseModel):
    """
    额外的请求混入
    """
    method: Method
    path: str
    prefix: str
    detail: bool
    view_type: ViewType
    response_schema: Type[BaseModel]
    permission: 'Permission'  # todo:增加权限支持
    __init: bool = False

    def __call__(self, *args, **kwargs):
        pass

    def init(self, router: APIRouter):
        """
        注册路由
        """
        self.__init = True
        pass
        # if self.method == Method.GET:
        #     @router.get(self.path, response_model=self.response_schema)
        #     async def request():
        #         return None
        #

    def get_openapi_json(self) -> dict:
        """
        生成该请求的openapi字符串
        """


class GetMixin(RequestMixin):
    method = Method.GET
    pass


from .page import LimitOffsetPaginator


class ListMixin(GetMixin):
    list_display: Iterable[str]
    view_type = ViewType.Grid
    paginator: Type[BaseModel] = LimitOffsetPaginator
    filter_classes: Tuple[str, ...]
    search_classes: Tuple[str, ...]

    def init(self, router: APIRouter):
        super(ListMixin, self).init(router)

        @router.get(self.path, response_model=self.response_schema)
        async def list(page: LimitOffsetPaginator, resource: str,
                       search: str = Depends(search_depend(self.search_classes)), **kwargs):
            model = get_model_from_str(resource)
            queryset = model.all().limit(page.limit).offset(page.offset)
            # todo:等待测试

    def __load_filter_field(self):
        pass

    def __load_search_field(self):
        pass
