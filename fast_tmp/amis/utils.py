from typing import List, Tuple, Type

from pydantic.main import BaseModel
from pydantic.schema import schema
from tortoise import Model
from tortoise.fields import BigIntField, CharField, IntField, SmallIntField
from tortoise.fields.data import CharEnumFieldInstance, DatetimeField, IntEnumFieldInstance

from fast_tmp.amis.schema.forms import Column
from fast_tmp.amis.schema.forms.enums import ControlEnum, FormWidgetSize, ItemModel
from fast_tmp.amis.schema.forms.widgets import (
    Control,
    DatetimeItem,
    NumberItem,
    SelectItem,
    SelectOption,
    TextItem,
)


def get_coulmns_from_pqc(
    list_schema: Type[BaseModel],
    include: Tuple[str, ...] = None,
    exclude: Tuple[str, ...] = None,
    add_type=False,
    extra_fields=None,
):
    """
    从pydantic_queryset_creator创建的schema获取字段
    extra_field:额外的自定义字段
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
                        if add_type:
                            res.append(
                                Control(
                                    name=field_name,
                                    label=fields[field_name]["title"],
                                    type=pf_2_jsf(fields[field_name]["type"]),
                                )
                            )
                        else:
                            res.append(Column(name=field_name, label=fields[field_name]["title"]))
    if extra_fields:
        res.append(*extra_fields)
    return res


def pf_2_jsf(field_type: str) -> str:
    """
    把python的字段类型转为js的类型
    """
    print(field_type)
    if field_type == "integer":
        return ControlEnum.number
    else:
        return ControlEnum.text


# fixme:等待修复
def get_coulmns_from_pmc(
    model_schema: Type[BaseModel],
    include: Tuple[str, ...] = None,
    exclude: Tuple[str, ...] = None,
    add_type: bool = False,
):
    """
    从pydantic_model_creator创建的schema获取字段
    """
    model_name = model_schema.__name__
    j1 = model_schema.schema()
    json_models = schema([model_schema])["definitions"]
    res: List[Column] = []
    for json_model in json_models:
        if json_model == model_name:
            items = json_models[json_model]["properties"]
            for k, v in items.items():
                if include:
                    if k not in include:
                        continue
                if exclude:
                    if k in exclude:
                        continue
                if add_type:
                    res.append(Control(name=k, label=v["title"], type=pf_2_jsf(v["type"])))
                else:
                    res.append(Column(name=k, label=v["title"]))
            break
    return res


# fixme:等待修复
def get_columns_from_str(
    fields: List[str], include: List[str] = None, exclude: List[str] = None, add_type: bool = False
) -> List[Column]:
    res = []
    for field in fields:
        res.append(Column(name=field, label=field))
    return res


def _get_base_attr(field_type) -> dict:
    return dict(
        className=field_type.kwargs.get("className", None),
        inputClassName=field_type.kwargs.get("inputClassName", None),
        labelClassName=field_type.kwargs.get("labelClassName", None),
        name=field_type.model_field_name,
        label=field_type.kwargs.get("verbose_name", field_type.model_field_name),
        labelRemark=field_type.kwargs.get("labelRemark", None),
        description=field_type.kwargs.get("description", None),
        placeholder=field_type.kwargs.get("placeholder", None),
        inline=field_type.kwargs.get("placeholder", False),
        submitOnChange=field_type.kwargs.get("submitOnChange", False),
        disabled=field_type.kwargs.get("disabled", False),
        disableOn=field_type.kwargs.get("disableOn", None),
        # validations=field_type.kwargs.get("validations", None),
        # validationErrors=field_type.kwargs.get("validationErrors", None),
        required=field_type.kwargs.get("required", True),
        mode=field_type.kwargs.get("mode", ItemModel.normal),
        size=field_type.kwargs.get("size", FormWidgetSize.md),
        value=getattr(field_type, "default", field_type.kwargs.get("default", None)),
    )


def get_columns_from_model(
    model: Type[Model],
    include: List[str] = None,
    exclude: List[str] = None,
    add_type: bool = False,
    extra_fields=None,
    exclude_readonly: bool = False,
):
    """
    从pydantic_queryset_creator创建的schema获取字段
    extra_field:额外的自定义字段
    """
    fields = model._meta.fields_map

    res = []
    for field, field_type in fields.items():
        if add_type:
            if exclude_readonly and field_type.pk:
                continue
            if isinstance(field_type, (IntField, SmallIntField, BigIntField)):
                if isinstance(field_type, IntEnumFieldInstance):
                    enum_type = field_type.enum_type
                    res.append(
                        SelectItem(
                            options=[
                                SelectOption(label=label, value=value)
                                for value, label in enum_type.choices.items()
                            ],
                            **_get_base_attr(field_type),
                        ),
                    )
                else:
                    res.append(
                        NumberItem(
                            min=field_type.kwargs.get("min", None)
                            or field_type.constraints.get("ge"),
                            max=field_type.kwargs.get("max", None)
                            or field_type.constraints.get("le"),
                            precision=field_type.kwargs.get("precision", 0),
                            step=field_type.kwargs.get("step", 1),
                            **_get_base_attr(field_type),
                            validations={
                                "minimum": field_type.kwargs.get("min", None)
                                or field_type.constraints.get("ge"),
                                "maximum": field_type.kwargs.get("max", None)
                                or field_type.constraints.get("le"),
                            },
                        ),
                    )
            elif isinstance(field_type, CharField):
                if isinstance(field_type, CharEnumFieldInstance):
                    enum_type = field_type.enum_type
                    res.append(
                        SelectItem(
                            options=[
                                SelectOption(label=label, value=value)
                                for value, label in enum_type.choices.items()
                            ],
                            **_get_base_attr(field_type),
                        ),
                    )
                else:
                    res.append(
                        TextItem(
                            **_get_base_attr(field_type),
                            validations={
                                "maxLength": field_type.kwargs.get("maxLength", None)
                                or field_type.max_length,
                            },
                        )
                    )
            # todo:等待完成,另，需要完成date
            elif isinstance(field_type, DatetimeField):
                res.append(
                    DatetimeItem(
                        **_get_base_attr(field_type),
                        format=field_type.kwargs.get("format", "YYYY-MM-DD HH:mm:ss"),
                        inputFormat=field_type.kwargs.get("inputFormat", "YYYY-MM-DD HH:mm:ss"),
                    )
                )
            elif isinstance(field_type, CharEnumFieldInstance):
                print(field_type.enum_type)
        else:
            res.append(Column(name=field, label=field_type.kwargs.get("verbose_name", field)))
    return res
