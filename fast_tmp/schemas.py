# -*- encoding: utf-8 -*-
"""
@File    : schemas.py
@Time    : 2021/1/11 16:48
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from enum import Enum
from typing import List, Optional, Type, Union

from pydantic.main import BaseModel


class PermissionPageType(str, Enum):
    page = "page"
    widget = "widget"
    route = "route"


class PermissionSchema(BaseModel):
    label: str
    codename: str = None
    type: PermissionPageType = PermissionPageType.widget
    children: List[Union["PermissionSchema", "SiteSchema"]] = []
    prefix: str = ""  # 基础理由


class SiteSchema(PermissionSchema):
    icon: Optional[str]
