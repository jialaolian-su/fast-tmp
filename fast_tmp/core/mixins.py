from typing import Dict, List, Optional, Tuple, Type, Union, cast

from fastapi import APIRouter, Depends, FastAPI
from pydantic import BaseModel
from tortoise import Model
from tortoise.contrib.pydantic import PydanticModel, pydantic_queryset_creator
from tortoise.query_utils import Q

from fast_tmp.amis.schema.abstract_schema import AmisModel
from fast_tmp.amis.schema.crud import CRUD
from fast_tmp.amis.utils import get_coulmns_from_pqc
from fast_tmp.choices import ElementType, Method
from fast_tmp.conf import settings
from fast_tmp.core.amis_router import AmisRouter
from fast_tmp.core.filter import DependField, filter_depend, search_depend
from fast_tmp.core.page import AmisPaginator, amis_paginator
from fast_tmp.utils.model import get_model_from_str

_SCHEMA_DICT: Dict[str, Type[BaseModel]] = {}


class RequestMixin(BaseModel):
    """
    额外的请求混入
    """

    method: Method
    path: str
    # detail: bool
    response_schema: Optional[BaseModel] = None
    permissions: Tuple[Union[str, "Permission"], ...] = ()  # todo:增加权限支持

    def init(
        self,
        router: AmisRouter,
    ):
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

    def init(self, router: Union[APIRouter, FastAPI]):
        pass


# class DeleteMixin(RequestMixin):
#     method = Method.DELETE
#     model: str
#
#     def init(self, router: Union[APIRouter, FastAPI]):
#         async def f(pk: str):
#             model = get_model_from_str(self.get)
#             await model.filter(pk=pk).delete()  # fixime:记得测试是否触发信号
#
#         f.__name__ = self.model + "_delete_mixin"
#         self.request_element_type[f.__name__] = ElementType.Null
#         router.delete(
#             self.path,
#         )(f)
#         return f


# fixme；需要重构为支持amis的结构
class ListMixin(GetMixin):
    filter_fields: Tuple[Union[DependField, str], ...] = ()
    search_fields: Tuple[str, ...] = ()
    order_fields: Tuple[str, ...] = ()  # fixme: 只支持单个排序
    model_str: str
    app_label: str = "models"
    include: Tuple[str, ...] = ()
    exclude: Tuple[str, ...] = ()  # 在include存在的情况下会忽略exclude

    def get_response_schema(self):
        if self.response_schema:
            return self.response_schema
        else:
            raise Exception("未实现")

    def get_filter_fields(self):
        return self.filter_fields

    def get_search_fields(self):
        return self.search_fields

    def get_queryset(self):
        return self.get_model().all()

    def get_model(self):
        model = get_model_from_str(self.model_str, self.app_label)
        return model


class AimsListMixin(ListMixin):
    paginator: Type[BaseModel] = AmisPaginator
    list_schema: BaseModel = None

    def init(self, router: AmisRouter):
        async def f(
            page: AmisPaginator = Depends(amis_paginator),
            search_field: Optional[str] = Depends(search_depend),
            filter_fields: dict = Depends(filter_depend(self.get_filter_fields())),
        ):
            model = self.get_model()
            count = await self.get_queryset().count()
            queryset = model.all().limit(page.perPage).offset(page.perPage * (page.page - 1))
            q = Q()
            # 搜索功能
            if search_field:  # fixme:考虑是否要把数字单独考虑
                for k in self.get_search_fields():  # 搜索功能
                    q |= Q(**{k + "__icontains": search_field})
                queryset = queryset.filter(q)
            for k, v in filter_fields.items():
                if v:
                    queryset = queryset.filter(**{k: v})
            return {
                "total": count,
                "items": await self.get_orm_list_schema().from_queryset(queryset),
            }

        view = self.get_amis_schema(router)
        f.__name__ = self.model_str + "_aims_list_mixin"
        router.get(self.path, view=view, response_model=self.get_response_schema())(f)
        return f

    def get_orm_list_schema(self):
        if self.list_schema:
            return self.list_schema
        model = self.get_model()
        if self.include:
            res_model = pydantic_queryset_creator(
                model, name=model.__name__ + "AdminList", include=self.include
            )
        elif self.exclude:
            res_model = pydantic_queryset_creator(
                model, name=model.__name__ + "AdminList", exclude=self.exclude
            )
        else:
            res_model = pydantic_queryset_creator(
                model,
                name=model.__name__ + "AdminList",
            )
        self.list_schema = res_model
        return res_model

    def get_response_schema(self):
        # fixme:考虑多对多一对多等字段的显示问题
        model = self.get_model()
        schema_name = model.__name__ + "AmisList"
        if _SCHEMA_DICT.get(schema_name, None):
            return _SCHEMA_DICT.get(schema_name)
        res_model = self.get_orm_list_schema()
        properties = {"__annotations__": {"total": int, "items": res_model}}
        return cast(Type[PydanticModel], type(schema_name, (PydanticModel,), properties))

    def get_amis_schema(self, router: AmisRouter) -> AmisModel:  # todo:存在一个bug导致数据无法正确渲染到页面
        sc = self.get_orm_list_schema()
        columns = get_coulmns_from_pqc(sc, include=self.include, exclude=self.exclude)
        return CRUD(
            api=settings.SERVER_URL + settings.ADMIN_URL + router.prefix + self.path,
            columns=columns,
        )


class RetrieveMixin(GetMixin):
    pass


class CreateMixin(PostMixin):
    def init(self, router: Union[APIRouter, FastAPI]):
        @router.post(
            self.path,
        )
        async def p(data):
            pass


class DestoryMixin(PostMixin):
    pass
