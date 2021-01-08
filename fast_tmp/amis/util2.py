from typing import List, Tuple, Type

from fast_tmp.amis.schema.forms import Column as FastColumn
from fast_tmp.amis.schema.forms import Control, FormWidgetSize, ItemModel
from fast_tmp.amis.schema.forms.widgets import NumberItem
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import ColumnProperty

# fixme: 这个为string子类
from sqlalchemy.types import Enum  # 注意用法
from sqlalchemy.types import Interval  # 时间段
from sqlalchemy.types import Unicode  # 在某些需要做索引的时候用这个更快，这是固定长度的unicode
from sqlalchemy.types import (
    ARRAY,
    DECIMAL,
    JSON,
    VARBINARY,
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    LargeBinary,
    PickleType,
    SmallInteger,
    String,
    Text,
    Time,
)


def _get_base_attr(column) -> dict:
    return dict(
        className=column.info.get("className", None),
        inputClassName=column.info.get("inputClassName", None),
        labelClassName=column.info.get("labelClassName", None),
        name=column.key,
        label=column.info.get("verbose_name", column.key),
        labelRemark=column.info.get("labelRemark", None),
        description=column.info.get("description", None),
        placeholder=column.info.get("placeholder", None),
        inline=column.info.get("inline", False),
        submitOnChange=column.info.get("submitOnChange", False),
        disabled=column.info.get("disabled", False),
        disableOn=column.info.get("disableOn", None),
        required=column.info.get("required", True),
        mode=column.info.get("mode", ItemModel.normal),
        size=column.info.get("size", FormWidgetSize.md),
    )


# todo:等待完成
def create_control(column, add_default_value) -> Control:
    if column.info.get("Control"):
        return column.info.get("Control")
    if isinstance(column.type, SmallInteger):
        return NumberItem(
            min=column.info.get("min", -32767),
            max=column.info.get("max", 32767),
            precision=column.info.get("precision", 0),
            step=column.info.get("step", 1),
            **_get_base_attr(column),
            value=column.default or None,
            validations={
                "minimum": column.info.get("min", -32767),
                "maximum": column.info.get("max", 32767),
            },
        )
    elif isinstance(column.type, BigInteger):
        pass
    elif isinstance(column.type, Integer):  # 整数，短整数，长整数
        return NumberItem(
            min=column.info.get("min", -2147483647),
            max=column.info.get("max", 2147483647),
            precision=column.info.get("precision", 0),
            step=column.info.get("step", 1),
            **_get_base_attr(column),
            value=column.default if add_default_value and column.default else None,
            validations={
                "minimum": column.info.get("min", -2147483647),
                "maximum": column.info.get("max", 2147483647),
            },
        )
    elif isinstance(column.type, Float):
        pass
    elif isinstance(column.type, DECIMAL):
        pass
    elif isinstance(column.type, ARRAY):
        pass
    elif isinstance(column.type, Boolean):  # 如果有默认值则渲染为switch，否则渲染为下拉
        pass
    elif isinstance(column.type, VARBINARY):
        pass
    elif isinstance(column.type, LargeBinary):
        pass
    elif isinstance(column.type, Interval):
        pass
    elif isinstance(column.type, Time):
        pass
    elif isinstance(column.type, DateTime):
        pass
    elif isinstance(column.type, Date):
        pass
    elif isinstance(column.type, JSON):
        pass
    elif isinstance(column.type, Enum):
        pass
    elif isinstance(column.type, Text):
        pass
    elif isinstance(column.type, Unicode):
        pass
    elif isinstance(column.type, String):
        pass
    elif isinstance(column.type, PickleType):
        pass
    else:
        raise Exception(f"Can't found this type:{column.type}")


def create_column(column) -> FastColumn:
    pass


def sqlalchemy_to_control(
        db_model: Type, *, include: Tuple[str] = (), exclude: Tuple[str] = (), add_type: bool = False,
        add_default_value: bool = False,
) -> List[Control]:
    mapper = inspect(db_model)
    res = []
    for attr in mapper.attrs:
        if isinstance(attr, ColumnProperty):
            if attr.columns:
                name = attr.key
                if (include and name not in include) or name in exclude:
                    continue
                column = attr.columns[0]
                if add_type:
                    if column.primary_key:
                        continue
                    res.append(create_control(column, add_default_value))
                else:
                    res.append(create_column(column))
            # python_type: Optional[type] = None
            #
            # if hasattr(column.type, "impl"):
            #     if hasattr(column.type.impl, "python_type"):
            #         python_type = column.type.impl.python_type
            # elif hasattr(column.type, "python_type"):
            #     python_type = column.type.python_type
            # assert python_type, f"Could not infer python_type for {column}"

    return res
