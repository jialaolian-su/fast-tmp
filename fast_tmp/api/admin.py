# -*- encoding: utf-8 -*-
"""
@File    : admin.py
@Time    : 2021/1/11 15:03
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import List

from fastapi import Depends

from fast_tmp.amis.utils import get_columns_from_model
from fast_tmp.amis_router import AmisRouter
from fast_tmp.depends import get_current_user
from fast_tmp.models import Group, Permission, User

admin_app = AmisRouter(prefix="/admin")


@admin_app.post("/user", summary="summary", description="desc")
async def create_user(username: str, password: str):
    user = User(username=username)
    user.set_password(password)
    await user.save()
    return


@admin_app.get("/site")
async def get_site(user: User = Depends(get_current_user)):
    """
    获取token
    :param user:
    :return:
    """
    permissions = await user.get_perms()
    print(permissions)
    from example.main import app

    site = app.permission
    return site


@admin_app.post("/permission")
async def create_permission(label: str, codename: str):
    p = await Permission.create(label=label, codename=codename)
    return p


@admin_app.post("/group")
async def create_group(label: str, users: List[int], permissions: List[int]):
    g = await Group.create(label=label)
    x = await Permission.filter(id__in=permissions)
    users = await User.filter(id__in=users)
    for user in users:
        await user.groups.add(g)
    await g.permissions.add(*x)
