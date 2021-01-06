from typing import Dict, List, Optional, Tuple, Union

from pydantic import HttpUrl
from pydantic.main import BaseModel

from fast_tmp.amis.schema.abstract_schema import _Action
from fast_tmp.amis.schema.forms import AbstractControl, Control
from fast_tmp.amis.schema.forms.enums import ControlEnum, FormWidgetSize, ItemModel


class AddControl(BaseModel):
    type: str = "text"
    name: str
    label: str


class Item(BaseModel):
    label: str
    value: Union[str, int]


class ItemValidation(BaseModel):  # 验证工具
    pass


class ItemValidationError(BaseModel):
    pass


class NumberItem(Control):
    type: ControlEnum = ControlEnum.number
    min: Optional[int]
    max: Optional[int]
    precision: int = 0  # 小数点后几位
    step: Optional[int]  # 选择的步长
    value: Optional[int]


class TextItem(Control):
    value: Optional[str]


class SelectOption(BaseModel):
    label: str
    value: Union[int, str]


class SelectItem(Control):
    type = ControlEnum.select
    options: Optional[List[Union[SelectOption, str, int]]]
    children: Optional[List[Union[SelectOption, str, int]]]  # 这个在树结构在考虑
    source: Optional[str]  # 通过数据源里面获取，也可以配置地址从远程获取，值格式为:options:[{label:..,value:...,}]
    multiple: bool = False  # 是否多选
    joinValues: Optional[bool]
    extractValue: Optional[bool]
    value: Optional[
        str
    ]  # 注意分割符保持一致,多选也可以配置返回数组格式，具体参考https://baidu.gitee.io/amis/docs/components/form/options#%E5%8A%A8%E6%80%81%E9%85%8D%E7%BD%AE
    searchable: bool = False  # 前端对选项是否启动搜索功能
    autoComplete: bool = True  # 是否对选项启动自动补全


class SelectItemCanModify(SelectItem):
    """
    可以修改选项值的选择器
    """

    creatable: bool = False  # 是否支持新增选项
    addControls: Tuple[AddControl, ...] = (
        AddControl(type="text", name="label", label="选项标题"),
        AddControl(type="text", name="value", label="选项值"),
    )  # 配置弹框信息，第一个为标题，第二个为选项值
    addApi: Optional[HttpUrl]  # 配置增加接口，如果为空则不会保存
    editable: bool = False  # 前端是否可编辑
    editControls: Tuple[AddControl, ...] = (
        AddControl(type="text", name="label", label="选项标题"),
        AddControl(type="text", name="value", label="选项值"),
    )  # 配置修改值的弹框信息
    editApi: Optional[HttpUrl]
    deleteApi: Optional[HttpUrl]  # 配置删除接口


class ArrayItem(Control):
    type: str = ControlEnum.array
    items: str = "text"  # 这个到时候改为枚举
    addable: bool = True  # 是否可新增
    removable: bool = True  # 是否可删除
    draggable: bool = False  # 是否可拖动排序，是否可以拖动排序, 需要注意的是当启用拖动排序的时候，会多一个$id 字段，具体请参考：https://baidu.gitee.io/amis/docs/components/form/array
    draggableTip: Optional[str]
    addButtonText: Optional[str]  # 新增按钮的文字
    minLength: Optional[int]  # 最短长度
    maxLength: Optional[int]  # 最长长度


class DatetimeItem(Control):
    type = ControlEnum.datetime
    value: Optional[str]
    format: str = "YYYY-MM-DD HH:mm:ss"  # 'X'为时间戳格式,参考文档：https://baidu.gitee.io/amis/zh-CN/docs/components/form/datetime
    inputFormat: str = "YYYY-MM-DD HH:mm:ss"  # 'X'为时间戳格式
    shortcuts: List[
        str
    ] = (
        []
    )  # "yesterday" ,"today", "tomorrow",now,{n}hoursago : n 小时前，例如：1daysago，下面用法相同,{n}hourslater : n 小时前，例如：1daysago
    utc: bool = False
    clearable: bool = True
    embed: bool = False  # fixme:学习内联如何使用
    timeConstrainst: bool = True  # 不知道干吗用的


class ButtonToolbar(AbstractControl):
    """
    按钮组
    """

    type = "button-toolbar"
    label: str = "按钮组"
    buttons: List[_Action]
