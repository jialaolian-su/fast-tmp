# -*- encoding: utf-8 -*-
"""
@File    : exceptions.py
@Time    : 2020/12/2 23:03
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""


# 这里记录http一般情况下的异常返回??
class ErrorException(Exception):
    pass


class UserBanedError(ErrorException):
    """
    用户被封禁
    """

    pass
