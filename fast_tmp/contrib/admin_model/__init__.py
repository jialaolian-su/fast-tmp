from fastapi import APIRouter
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import ModelMeta
from typing import Optional

from fast_tmp.contrib.admin_model.paginator import Paginator


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
        if name == 'BaseModelAdmin':
            return type.__new__(cls, name, bases, attrs)
        attrs['__name__'] = name
        return type.__new__(cls, name, bases, attrs)


class BaseModelAdmin(metaclass=MediaMetaClass):
    model = None
    action: Optional[APIRouter] = None

    def create_func(self):
        @self.action.post("", response_model=self.get_create_schema(), summary='创建', )
        async def create()

    def get_create_schema(self,in):
        schema_name = self.__name__ + 'Create'
        schema = pydantic_model_creator(self.model, name=schema_name, exclude=('id',))  # todo:增加pk字段的过滤，这样可以兼容pk不为id的情况
        return schema


class ModelAdmin:
    model: ModelMeta
    methods = ["create", "delete", "update", "delete", "retrieve"]  # put
    list_display = ("__str__",)
    # list_display_links = ()
    list_filter = ()  # 过滤字段
    list_select_related = False  # 链接外键的信息
    list_per_page = 10  # list页面默认显示值
    list_max_show_all = 200  # list页面最大显示值
    list_editable = ()  # 页面可编辑
    search_fields = ()  # 搜索字段
    date_hierarchy = None
    save_as = False
    save_as_continue = True
    save_on_top = False
    # 分页功能
    paginator = Paginator
    preserve_filters = True
    inlines = []  # 内联显示？

    # Custom templates (designed to be over-ridden in subclasses)
    add_form_template = None
    change_form_template = None
    change_list_template = None
    delete_confirmation_template = None
    delete_selected_confirmation_template = None
    object_history_template = None
    popup_response_template = None

    # Actions
    actions = []
    # action对应的ser
    # action_form = helpers.ActionForm
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True

    # checks_class = ModelAdminChecks

    def get_route_conf(self):
        """
        获取路由配置，包括字段、枚举等信息
        :return:
        """

    def get_ser_class(self):
        pass

    def get_ser(self):
        pass

    def get_queryset(self):
        pass
