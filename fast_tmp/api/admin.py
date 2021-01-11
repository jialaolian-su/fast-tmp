# -*- encoding: utf-8 -*-
"""
@File    : admin.py
@Time    : 2021/1/11 15:03
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""

from fast_tmp.amis_router import AmisRouter

from fast_tmp.models import User

admin_app = AmisRouter(prefix="/admin")


@admin_app.post("/user", )
async def create_user(username: str, password: str):
    user = User(username=username)
    user.set_password(password)
    await user.save()
    return
