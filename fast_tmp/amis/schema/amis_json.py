# -*- encoding: utf-8 -*-
"""
@File    : amis_json.py
@Time    : 2021/1/2 21:32
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fast_tmp.amis.schema.abstract_schema import BaseAmisModel


class Json(BaseAmisModel):
    type = "json"
    source: str
