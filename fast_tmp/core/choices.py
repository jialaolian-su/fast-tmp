from enum import Enum


class Method(str, Enum):
    """
    请求类型
    """
    GET = 'GET'
    POST = 'POST'


class ViewType(str, Enum):
    """
    在页面显示为什么东西
    """
    Button = 'Button'
    Grid = 'Grid'

