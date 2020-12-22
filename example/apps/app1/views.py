# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/12/2 23:10
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from datetime import datetime
from typing import Type

from fastapi import APIRouter, Depends, Form
from tortoise import Model

from example.serializers import Author1, Author2, BOOK2, BOOK1
from example.apps.app1.serializer import LoginInfoSer, LoginInfoSer2
from fast_tmp.contrib.admin_model import ModelAdmin
from example.models import Team

router = APIRouter()


@router.post("/login", summary="登录", response_model=LoginInfoSer)
async def login(userinfo: LoginInfoSer):
    print(userinfo)
    return {"code": 200}


@router.post("/user", summary="用户信息", response_model=LoginInfoSer2)
async def userinfo(username: LoginInfoSer2):
    return


@router.post("/group", response_model=Author1)
async def group(group1: Author1):
    return group1


@router.post("/group2", response_model=Author2)
async def group2(group2: Author2):
    return group2


@router.post("/book1", response_model=BOOK1)
async def book1(book1: BOOK1, **kwargs):
    return book1


class PDepends(object):
    def __init__(self, queryset: str):
        """
        应该在AdminType初始化的时候，直接把对应的queryset写入到init里面，这样在使用的时候直接用depends依赖该函数即可。
        :param queryset:
        :param limit:
        :param offset:
        """
        self.queryset = queryset

    def __call__(self, s: str) -> str:
        return self.queryset + s
