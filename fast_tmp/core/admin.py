# -*- encoding: utf-8 -*-
"""
@File    : admin.py
@Time    : 2020/12/20 23:13
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import List, Dict, Type, Any, Callable
from .mixins import RequestMixin
from tortoise import Model

from fastapi import FastAPI, APIRouter


class AdminApp(FastAPI):
    """
    继承增加新功能
    """
    models: Dict[str, Type[Model]] = {}
    list_display: List[str]
    user_model: Type[Model]
    permission_model: Type[Model]
    role_model: Type[Model]
    admin_log_model: Type[Model]
    extra_request: Type[RequestMixin]
