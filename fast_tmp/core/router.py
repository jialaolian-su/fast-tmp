# -*- encoding: utf-8 -*-
"""
@File    : router.py
@Time    : 2020/12/20 22:55
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import Tuple

from fastapi import APIRouter, Depends

from .page import limit_offset_paginator

router = APIRouter(prefix="/rest")


@router.get("/{model_name}")
async def list(page: Tuple[int, int] = Depends(limit_offset_paginator), **kwargs):
    pass
