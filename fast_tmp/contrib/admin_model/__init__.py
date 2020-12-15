from fastapi import APIRouter, Depends
from pydantic import BaseModel
from tortoise import QuerySet
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from typing import Optional, List, Type, Sequence, Any, Union, Tuple

from fast_tmp.contrib.admin_model.paginator import Paginator, PaginatorDepends


class MediaMetaClass(type):
    """
    处理一部分信息
    """

    # def __new__(mcs, name, bases, attrs):
    #     new_class = super().__new__(mcs, name, bases, attrs)
    #
    #     if 'media' not in attrs:
    #         new_class.media = media_property(new_class)
    #
    #     return new_class
    def __new__(cls, name, bases, attrs):
        attrs['__name__'] = name
        new_class = type.__new__(cls, name, bases, attrs)
        if attrs.get("paginator"):
            list_queryset = attrs.get("get_queryset")(new_class)
            attrs['paginator'] = attrs.get("paginator")(list_queryset)
        return new_class


class BaseModelAdmin(metaclass=MediaMetaClass):
    model = None
    action: Optional[APIRouter] = None

    def create_func(self):
        pass

    def get_create_schema(self, ):
        pass


class ModelAdmin:
    prefix: str
    router: APIRouter
    model: Model
    methods = ["create", "delete", "update", "delete", "retrieve"]  # put
    list_display = ("__str__",)
    # list_display_links = ()
    list_filter = ()  # 过滤字段
    list_select_related = False  # 链接外键的信息
    list_per_page = 10  # list页面默认显示值
    list_max_show_all = 200  # list页面最大显示值
    list_editable = ()  # 可页面编辑
    search_fields = ()  # 搜索字段
    date_hierarchy = None
    save_as = False
    save_as_continue = True
    save_on_top = False
    # 分页功能
    # paginator = PaginatorDepends
    paginator: Optional[PaginatorDepends] = None
    preserve_filters = True
    inlines: List[str] = []  # 内联显示？

    # Custom templates (designed to be over-ridden in subclasses)
    add_form_template = None
    change_form_template = None
    change_list_template = None
    delete_confirmation_template = None
    delete_selected_confirmation_template = None
    object_history_template = None
    popup_response_template = None

    # Actions
    actions: List[str] = []
    # action对应的ser
    # action_form = helpers.ActionForm
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True

    # checks_class = ModelAdminChecks
    def get_model(self) -> Type[Model]:
        pass

    def get_route_conf(self):
        """
        获取路由配置，包括字段、枚举等信息
        :return:
        """

    def get_preifx(self, action: str) -> str:
        """
        获取请求路径
        :param action:create,list等
        :return:
        """
        pass

    def get_ser_class(self, action: str) -> Union[Tuple[Type[BaseModel], Type[BaseModel]], Type[BaseModel]]:
        model = self.get_model()
        if action == 'create':
            request_schema = pydantic_model_creator(model, exclude_readonly=True, name=model.__name__ + "_Post_Request")
            response_schema = pydantic_model_creator(model, exclude_readonly=True,
                                                     name=model.__name__ + "_Post_Response")
            return request_schema, response_schema
        elif action == 'list':
            return pydantic_model_creator(model, include=self.list_display, name=model.__name__ + "_Get_List",
                                          allow_cycles=True, )

    def get_ser(self):
        pass

    def get_queryset(self) -> Model:
        pass

    def create(self):
        create_request_ser, create_response_ser = self.get_ser_class('create')
        model: Model = self.model

        @self.router.post(self.get_preifx('create'), response_model=create_response_ser)
        async def create_func(data: create_request_ser) -> Model:
            d: BaseModel = data
            ret = await model.create(**d.dict())
            return ret

        return create_func

    def list(self):
        list_response_ser: Type[BaseModel] = self.get_ser_class('list')

        @self.router.get(self.get_preifx('list'), response_model=list_response_ser)
        async def list_func(queryset: QuerySet[Model] = Depends(self.paginator)) -> List[Model]:
            ret = await queryset
            return ret

        return list_func

    def retrieve(self):
        retrieve_response_ser: Type[BaseModel] = self.get_ser_class('retrieve')

        @self.router.get(self.get_preifx('retrieve'), response_model=retrieve_response_ser)
        async def retrieve_func(pk: str) -> Model:
            ret = await self.get_queryset().get(pk=pk)
            return ret

        return retrieve_func

    def delete(self):
        @self.router.delete(self.get_preifx('delete'), )
        async def delete_func(pk: str):  # todo:确认一下增删改查是否会触发信号
            await self.get_queryset().filter(pk=pk).delete()

        return delete_func

    def partial_update(self):
        # todo:考虑字段为修改为空的问题
        par_update_request_ser, par_update_response_ser = self.get_ser_class('retrieve')
        # @self.router.patch(self.get_preifx('par_update'), response_model=par_update_response_ser)
        # async def par_update_func(pk: str, data: par_update_request_ser):
        #     await self.model.filter(pk=pk).update(par_update_request_ser.dict(unse))
        # return par_update_func
