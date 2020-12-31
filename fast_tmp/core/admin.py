# -*- encoding: utf-8 -*-
"""
@File    : admin.py
@Time    : 2020/12/20 23:13
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import Any, Callable, Dict, List, Optional, Type

from fastapi import APIRouter, FastAPI
from tortoise import Model

from fast_tmp.conf import settings

from ..choices import ElementType
from .mixins import RequestMixin


class AdminApp(FastAPI):
    request_element_type: Dict[str, ElementType] = {}
    models: Dict[str, Type[Model]] = {}
    user_model: Type[Model]
    permission_model: Type[Model]
    role_model: Type[Model]
    admin_log_model: Type[Model]
    extra_request: Type[RequestMixin]
    admin_log_model: Type[Model]
    # site: Site
    permission: bool
    admin_log: bool
    _inited: bool = False
    _field_type_mapping = {
        "IntField": "number",
        "BooleanField": "checkbox",
        "DatetimeField": "datetime",
        "DateField": "date",
        "IntEnumFieldInstance": "select",
        "CharEnumFieldInstance": "select",
        "DecimalField": "number",
        "FloatField": "number",
        "TextField": "textarea",
        "SmallIntField": "number",
        "JSONField": "json",
    }

    # model_menu_mapping: Dict[str, Menu] = {}

    # def _get_model_menu_mapping(self, menus: List[Menu]):
    #     for menu in filter(lambda x: (x.url and "rest" in x.url) or x.children, menus):
    #         if menu.children:
    #             self._get_model_menu_mapping(menu.children)
    #         else:
    #             self.model_menu_mapping[menu.url.split("?")[0].split("/")[-1]] = menu

    def _get_model_fields_type(self, model: Type[Model]) -> Dict:
        model_describe = model.describe()
        ret = {}
        data_fields = model_describe.get("data_fields")
        pk_field = model_describe.get("pk_field")
        fk_fields = model_describe.get("fk_fields")
        m2m_fields = model_describe.get("m2m_fields")
        fields = [pk_field] + data_fields + fk_fields + m2m_fields
        for field in fields:
            ret[field.get("name")] = self._get_field_type(
                field.get("name"), field.get("field_type")
            )
        return ret

    # def _build_content_menus(self) -> List[Menu]:
    #     menus = []
    #     for model_name, model in get_all_models():
    #         if issubclass(model, (AbstractUser, AbstractPermission, AbstractRole)):
    #             continue
    #         menu = Menu(
    #             name=model._meta.table_description or model_name,
    #             url=f"/rest/{model_name}",
    #             fields_type=self._get_model_fields_type(model),
    #             icon="icon-list",
    #             bulk_actions=[{"value": "delete", "text": "delete_all"}],
    #         )
    #         menus.append(menu)
    #     return menus

    # def _build_default_menus(self, permission=True):
    #     """
    #     build default menus when menus config not set
    #     :return:
    #     """
    #
    #     menus = [
    #         Menu(name="Home", url="/", icon="fa fa-home"),
    #         Menu(name="Content", children=self._build_content_menus()),
    #         Menu(
    #             name="External",
    #             children=[
    #                 Menu(
    #                     name="Github",
    #                     url="https://github.com/long2ice/fastapi-admin",
    #                     icon="fa fa-github",
    #                     external=True,
    #                 ),
    #             ],
    #         ),
    #     ]
    #     if permission:
    #         permission_menus = [
    #             Menu(
    #                 name="Auth",
    #                 children=[
    #                     Menu(
    #                         name="User",
    #                         url="/rest/User",
    #                         icon="fa fa-user",
    #                         search_fields=("username",),
    #                     ),
    #                     Menu(name="Role", url="/rest/Role", icon="fa fa-group",),
    #                     Menu(name="Permission", url="/rest/Permission", icon="fa fa-user-plus",),
    #                     Menu(name="Logout", url="/logout", icon="fa fa-lock",),
    #                 ],
    #             ),
    #         ]
    #         menus += permission_menus
    #     return menus

    # async def init(
    #     self,
    #     site: Site,
    #     admin_secret: str,
    #     permission: bool = False,
    #     admin_log: bool = False,
    #     login_view: Optional[str] = None,
    # ):
    #     """
    #     init admin site
    #     :param admin_log:
    #     :param login_view:
    #     :param permission: active builtin permission
    #     :param site:
    #     :param admin_secret: admin jwt secret.
    #     :return:
    #     """
    #     self.site = site
    #     self.permission = permission
    #     self.admin_secret = admin_secret
    #     self.admin_log = admin_log
    #     for model_name, model in get_all_models():
    #         if issubclass(model, AbstractUser):
    #             self.user_model = model
    #         elif issubclass(model, AbstractAdminLog):
    #             self.admin_log_model = model
    #         self.models[model_name] = model
    #     self._inited = True
    #     if not site.menus:
    #         site.menus = self._build_default_menus(permission)
    #     if permission:
    #         await self._register_permissions()
    #     self._get_model_menu_mapping(site.menus)
    #     if login_view:
    #         self.add_api_route("/login", import_obj(login_view), methods=["POST"])
    #     else:
    #         self.add_api_route("/login", login, methods=["POST"])
    #
    # async def _register_permissions(self):
    #     permission_model = None
    #     for model_name, model in get_all_models():
    #         if issubclass(model, AbstractPermission):
    #             permission_model = model
    #             break
    #     if not permission_model:
    #         raise Exception("No Permission Model Founded.")
    #
    #     for model, _ in get_all_models():
    #         for action in enums.PermissionAction.choices():
    #             label = f"{enums.PermissionAction.choices().get(action)} {model}"
    #             defaults = dict(label=label, model=model, action=action,)
    #             await permission_model.get_or_create(**defaults,)

    def _exclude_field(self, resource: str, field: str):
        """
        exclude field by menu include and exclude
        :param resource:
        :param field:
        :return:
        """
        menu = self.model_menu_mapping[resource]
        if menu.include:
            if field not in menu.include:
                return True
        if menu.exclude:
            if field in menu.exclude:
                return True
        return False

    def register_mixin(self, mixin: RequestMixin):
        mixin.init(self)
        self.request_element_type.update(mixin.request_element_type)


admin_app = AdminApp(
    debug=False,
    title="FastAPI-Admin",
    root_path="/admin",
    description="FastAPI Admin Dashboard based on FastAPI and Tortoise ORM.",
)
from fast_tmp.utils.openapi import get_openapi

from .mixins import AimsListMixin
