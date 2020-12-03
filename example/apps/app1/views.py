# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/12/2 23:10
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fastapi import APIRouter, Depends, Form

from example.apps.app1.serializer import LoginInfoSer

router = APIRouter()


class LoginInfoForm():
    def __init__(self, username: str = Form(...,max_length=1), password: str = Form(...)):
        self.username = username
        self.password = password


@router.post("/login", summary="登录")
async def login(userinfo: LoginInfoForm = Depends()):
    print(userinfo)
    return {"code": 200}
