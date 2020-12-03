# -*- encoding: utf-8 -*-
"""
@File    : action.py
@Time    : 2020/12/3 22:05
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fastapi.routing import APIRoute
from starlette.responses import JSONResponse, Response

from typing import Optional, Type, Any, List, Sequence, Dict, Union, Set, Callable
from fastapi import params
from fastapi.encoders import DictIntStrAny, SetIntStr, jsonable_encoder

from fastapi import APIRouter

router = APIRouter()
from functools import wraps


class action:
    @classmethod
    def post(cls, path: str, *, response_model: Optional[Type[Any]] = None,
             status_code: int = 200,
             tags: Optional[List[str]] = None,
             dependencies: Optional[Sequence[params.Depends]] = None,
             summary: Optional[str] = None,
             description: Optional[str] = None,
             response_description: str = "Successful Response",
             responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
             deprecated: Optional[bool] = None,
             operation_id: Optional[str] = None,
             response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
             response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
             response_model_by_alias: bool = True,
             response_model_exclude_unset: bool = False,
             response_model_exclude_defaults: bool = False,
             response_model_exclude_none: bool = False,
             include_in_schema: bool = True,
             response_class: Optional[Type[Response]] = None,
             name: Optional[str] = None,
             callbacks: Optional[List[APIRoute]] = None,
             ) -> Callable:
        pass

    @classmethod
    def get(
            cls,
            path: str,
            *,
            response_model: Optional[Type[Any]] = None,
            status_code: int = 200,
            tags: Optional[List[str]] = None,
            dependencies: Optional[Sequence[params.Depends]] = None,
            summary: Optional[str] = None,
            description: Optional[str] = None,
            response_description: str = "Successful Response",
            responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
            deprecated: Optional[bool] = None,
            operation_id: Optional[str] = None,
            response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
            response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: Optional[Type[Response]] = None,
            name: Optional[str] = None,
            callbacks: Optional[List[APIRoute]] = None,
    ) -> Callable:
        pass