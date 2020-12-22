from typing import List, Dict, Type, Any, Callable, Iterable, Tuple, Union, Optional
from enum import Enum
from pydantic import BaseModel
from pydantic.utils import get_model
from tortoise import Model
from fastapi import APIRouter, Depends, FastAPI
from tortoise.query_utils import Q

from .choices import Method, ViewType
from .filter import search_depend, DependField, filter_depend, SearchValue
from ..contrib import get_user_model
from ..utils.model import get_model_from_str

User = get_user_model()


class RequestMixin(BaseModel):
    """
    额外的请求混入
    """
    method: Method
    path: str
    prefix: str
    # detail: bool
    view_type: ViewType
    response_schema: Type[BaseModel] = ()
    permissions: Tuple[Union[str, 'Permission'], ...] = ()  # todo:增加权限支持
    __init: bool = False

    def __call__(self, *args, **kwargs):
        pass

    def init(self, router: Union[APIRouter, FastAPI]):
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

    def has_perm(self, user_id: int):
        pass


class GetMixin(RequestMixin):
    method = Method.GET
    pass


from .page import LimitOffsetPaginator, limit_offset_paginator


class ListMixin(GetMixin):
    list_display: Iterable[str] = ()
    view_type = ViewType.Grid
    filter_classes: Tuple[Union[DependField, str], ...] = ()
    search_classes: Tuple[Union[DependField, str], ...] = ()
    order_classes: Tuple[str, ...] = ()  # fixme: 注意要考虑一下是否支持多个排序

    def init(self, router: APIRouter):  # fixme:等待修复
        pass

    def get_list_response_schema(self):
        return self.response_schema

    def get_filter_classes(self):
        return self.filter_classes

    def get_search_classes(self):
        return self.search_classes


class ListLimitOffsetMixin(ListMixin):
    paginator: Type[BaseModel] = LimitOffsetPaginator
    model: str

    def init(self, router: APIRouter):  # todo:等待测试
        # @router.get(self.path, response_model=self.get_list_response_schema())
        # async def list(resource: str, page: LimitOffsetPaginator = Depends(limit_offset_paginator),
        #                search_fields: dict = Depends(search_depend(self.get_search_classes())),
        #                filter_fields: dict = Depends(filter_depend(self.get_filter_classes()))):
        @router.get(self.path, response_model=self.get_list_response_schema())
        async def list(page: LimitOffsetPaginator = Depends(limit_offset_paginator),
                       search_field: Optional[SearchValue] = Depends(search_depend(self.get_search_classes())), ):
            model = get_model_from_str(self.model)
            count = await model.all().count()
            queryset = model.all().limit(page.limit).offset(page.offset)
            q = Q()
            # 搜索功能
            if search_field:
                for k in search_field.search_fields:  # 搜索功能
                    q |= Q(**{k: search_field.value})
                queryset = queryset.filter(q)
            # for k, v in filter_fields.items():
            #     queryset = queryset.filter(**{k: v})
            return {
                "count": count,
                "data": await queryset
            }
