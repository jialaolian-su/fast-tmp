# -*- encoding: utf-8 -*-
"""
@File    : page.py
@Time    : 2020/12/20 22:57
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from pydantic.main import BaseModel


class AmisPaginator(BaseModel):
    page: int
    perPage: int


def amis_paginator(page: int = 1, perPage: int = 10) -> AmisPaginator:
    return AmisPaginator(page=page, perPage=perPage)
