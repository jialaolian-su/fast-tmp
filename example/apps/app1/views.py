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

from example.apps.app1.serializer import LoginInfoSer

router = APIRouter()


class LoginInfoForm():
    def __init__(self, username: str = Form(..., max_length=1), password: str = Form(...)):
        self.username = username
        self.password = password


class Login2(BaseModel):
    username: str
    d: datetime = Field(..., )


@router.post("/login", summary="登录", response_model=Login2)
async def login(userinfo: LoginInfoForm = Depends()):
    print(userinfo)
    return {"code": 200}


class UserInfo(BaseModel):
    """用户信息"""
    name: str
    nickname: str
    age: int


@router.get("/user", summary="用户信息", response_model=UserInfo)
async def userinfo(username: Login2):
    return
