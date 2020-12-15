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

from fastapi import APIRouter, Depends, Form
from pydantic.main import BaseModel
from pydantic import Field
from example.serializers import Author1, Author2, BOOK2, BOOK1
from example.apps.app1.serializer import LoginInfoSer, LoginInfoSer2, GroupSer, GroupSer2

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
async def book1(book1: BOOK1,):
    return book1


@router.post("/book2", response_model=BOOK2)
async def book2(book2: BOOK2):
    return book2
