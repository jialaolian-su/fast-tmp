# -*- encoding: utf-8 -*-
"""
@File    : serializer.py
@Time    : 2020/12/2 23:12
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
# 存储数据的序列化器
from tortoise.contrib.pydantic import pydantic_model_creator

from example.models import User,Role

LoginInfoSer = pydantic_model_creator(User, name='LoginInfoSer')
LoginInfoSer2 = pydantic_model_creator(User, exclude_readonly=True, name='LoginInfoSer2')

