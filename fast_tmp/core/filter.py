import inspect
from typing import Any, Callable, List, Optional, Tuple, Type, Union

from pydantic.main import BaseModel


class DependField(BaseModel):
    field_name: str
    lookup_expr: Optional[str]  # 搜索按照这个字段来
    field_type: Type[Any] = str  # 字段类型

    def __str__(self):
        if self.lookup_expr:
            return self.field_name + "__" + self.lookup_expr
        else:
            return self.field_name


class SearchValue(BaseModel):
    search_fields: List[str]
    value: str


def search_depend(search: Optional[str] = None) -> Optional[str]:
    """
    搜索依赖
    """
    return search


def filter_depend(fields: Tuple[Union[DependField, str], ...]) -> Callable:
    """
    过滤依赖
    """

    def f(**kwargs):
        return kwargs

    parameters = []
    for field in fields:
        if isinstance(field, DependField):
            p = inspect.Parameter(
                field.field_name,
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=None,
                annotation=Optional[field.field_type],
            )  # fixme:考虑一下枚举、数字、字符串、时间怎么区分？是否自动查询
        else:
            p = inspect.Parameter(
                field, kind=inspect.Parameter.KEYWORD_ONLY, default=None, annotation=Optional[str]
            )  # fixme:考虑一下枚举、数字、字符串、时间怎么区分？是否自动查询
        parameters.append(p)
    f.__signature__ = inspect.Signature(parameters=parameters, return_annotation=dict)  # 依赖
    return f


def order_depend(model_name, fields: List[str]):
    """
    排序依赖
    """
