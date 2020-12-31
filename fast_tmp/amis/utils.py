from typing import List, Tuple, Type

from pydantic.main import BaseModel
from pydantic.schema import schema

from fast_tmp.amis.schema.widgets import Column


def get_coulmns_from_pqc(
    list_schema: Type[BaseModel], include: Tuple[str, ...] = None, exclude: Tuple[str, ...] = None
):
    """
    从pydantic_queryset_creator创建的schema获取字段
    """
    model_name = list_schema.__name__
    json_models = schema([list_schema])["definitions"]
    res: List[Column] = []
    for json_model in json_models:
        if json_model == model_name:
            items = json_models[json_model]["items"]
            for k, v in items.items():
                if k == "$ref":
                    m = json_models[v.split("/")[-1]]
                    fields = m["properties"]
                    for field_name in fields:
                        if include:
                            if field_name not in include:
                                continue
                        elif exclude:
                            if field_name in exclude:
                                continue
                        res.append(Column(name=field_name, label=fields[field_name]["title"]))
    return res


def get_coulmns_from_pmc(
    model_schema: Type[BaseModel], include: List[str] = None, exclude: List[str] = None
):
    """
    从pydantic_model_creator创建的schema获取字段
    """
    model_name = model_schema.__name__
    json_models = schema([model_schema])["definitions"]
    res: List[Column] = []
    for json_model in json_models:
        if json_model == model_name:
            items = json_models[json_model]["properties"]
            for k, v in items.items():
                res.append(Column(name=k, label=v["title"]))
            break
    return res


def get_columns_from_str(fields: List[str]) -> List[Column]:
    res = []
    for field in fields:
        res.append(Column(name=field, label=field))
    return res
