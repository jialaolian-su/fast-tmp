# -*- encoding: utf-8 -*-
"""
@File    : testpyandatic.py
@Time    : 2020/12/6 12:28
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from pydantic import Field
from pydantic.main import BaseModel


class A(BaseModel):
    a: str = Field(
        ...,
    )


a = A(a="4")


class B(A):
    a: int


b = B(a=3)
print(a.dict())
print(b.dict())
