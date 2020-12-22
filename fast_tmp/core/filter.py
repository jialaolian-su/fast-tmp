from typing import List, Union, Optional, Any, Type, Tuple
import inspect

from pydantic.main import BaseModel


class DependField(BaseModel):
    field_name: str
    lookup_expr: str  # 搜索按照这个字段来
    field_type: Type[Any] = str  # 字段类型


class SearchValue(BaseModel):
    search_fields: List[str]
    value: str


# todo:等待完成和测试
def search_depend(fields: Tuple[Union[DependField, str], ...]) -> Optional[SearchValue]:
    """
    搜索依赖
    """

    def f(search: str = None):
        if search is not None:
            res = []
            for field in fields:
                res.append(field)
            return SearchValue(search_fields=res, value=search)
        else:
            return None

    return f


def filter_depend(fields: Tuple[Union[DependField, str], ...]):
    """
    过滤依赖
    """

    def f(**kwargs):
        return kwargs

    parameters = []
    for field in fields:
        if isinstance(field, DependField):
            p = inspect.Parameter(field.field_name, kind=inspect.Parameter.KEYWORD_ONLY, default=None,
                                  annotation=Optional[field.field_type])  # fixme:考虑一下枚举、数字、字符串、时间怎么区分？是否自动查询
        else:
            p = inspect.Parameter(field, kind=inspect.Parameter.KEYWORD_ONLY, default=None,
                                  annotation=Optional[str])  # fixme:考虑一下枚举、数字、字符串、时间怎么区分？是否自动查询
        parameters.append(p)
    f.__signature__ = inspect.Signature(parameters=parameters, return_annotation=dict)  # 依赖
    return f


def order_depend(model_name, fields: List[str]):
    """
    排序依赖
    """
