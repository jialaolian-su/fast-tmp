from typing import List, Dict, Type, Any, Callable, Iterable, Tuple, Union, Optional
from enum import Enum
from pydantic import BaseModel
from pydantic.utils import get_model
from tortoise import Model
from fastapi import APIRouter, Depends, FastAPI
from tortoise.query_utils import Q
from .page import LimitOffsetPaginator, limit_offset_paginator
from fast_tmp.choices import Method, ElementType
from .filter import search_depend, DependField, filter_depend, SearchValue
from ..utils.model import get_model_from_str



class RequestMixin(BaseModel):
    """
    额外的请求混入
    """
    method: Method
    path: str
    prefix: str
    # detail: bool
    element_type: ElementType
    response_schema: Type[BaseModel] = ()
    permissions: Tuple[Union[str, 'Permission'], ...] = ()  # todo:增加权限支持
    request_element_type: Dict[str, ElementType] = {}  # 记录请求的类型

    def __call__(self, *args, **kwargs):
        pass

    def init(self, router: Union[APIRouter, FastAPI]):
        """
        注册路由
        """
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


class PostMixin(RequestMixin):
    method = Method.POST
    model: str
    post_include_fileds: List[str] = []
    post_exclude_fields: List[str] = []  # fixme:考虑把枚举作为请求接口进行返回

    def get_create_schema(self):
        pass

    def get_response_schema(self):
        pass

    def init(self, router: Union[APIRouter, FastAPI]):
        pass


class DeleteMixin(RequestMixin):
    method = Method.DELETE
    model: str

    def init(self, router: Union[APIRouter, FastAPI]):
        async def f(pk: str):
            model = get_model_from_str(self.model)
            await model.filter(pk=pk).delete()  # fixime:记得测试是否触发信号

        f.__name__ = self.model + "_delete_mixin"
        self.request_element_type[f.__name__] = ElementType.Null
        router.delete(self.path, )(f)
        return f


class ListMixin(GetMixin):
    list_display: Iterable[str] = ("__str__",)
    element_type = ElementType.Grid
    filter_classes: Tuple[Union[DependField, str], ...] = ()
    search_classes: Tuple[Union[DependField, str], ...] = ()
    order_classes: Tuple[str, ...] = ()  # fixme: 注意要考虑一下是否支持多个排序

    def init(self, router: APIRouter):  # fixme:等待初始化
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
        async def f(page: LimitOffsetPaginator = Depends(limit_offset_paginator),
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

        f.__name__ = self.model + "_limit_offset_list_mixin"
        router.get(self.path, response_model=self.get_list_response_schema())(f)
        self.request_element_type[f.__name__] = ElementType.Grid
        return f


class RetrieveMixin(GetMixin):
    pass


class CreateMixin(PostMixin):

    def init(self, router: Union[APIRouter, FastAPI]):
        @router.post(self.path, )
        async def p(data):
            pass


class DestoryMixin(PostMixin):
    pass

class ModelAdmin(ListLimitOffsetMixin, ):
    pass
