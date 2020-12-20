# -*- encoding: utf-8 -*-
"""
@File    : page.py
@Time    : 2020/12/20 22:57
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import Tuple


def limit_offset_paginator(limit: int, offset: int) -> Tuple[int, int]:
    return limit, offset
