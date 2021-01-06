from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from fast_tmp.amis.schema.abstract_schema import BaseAmisModel
from fast_tmp.amis.schema.enums import TypeEnum
from fast_tmp.amis.schema.forms.enums import ControlEnum, FormWidgetSize, ItemModel


# fixme:未来考虑更多的fields类型字段支持
class Column(BaseModel):
    """
    用于列表等的显示
    """

    name: str
    label: str


class AbstractControl(Column):
    pass


class Form(BaseAmisModel):
    type = TypeEnum.form
    controls: List[AbstractControl]
    name: str
    title: str = "表单"
    submitText: str = "提交"
    # className:str
    # actions: Optional[List[_Action]]
    # messages: Optional[Message]#自定义返回信息加这个字段
    wrapWithPanel: bool = True
    api: str
    initApi: Optional[str]
    # interval: int = 3000??
    primaryField: str = "id"  # 设置主键


# todo:等待完成
class Control(AbstractControl):
    """
    用户form表单等写入
    """

    type: ControlEnum = ControlEnum.text  # 把这个和schema获取的参数进行融合，保证schema获取的值可以使用
    name: str
    label: Optional[str]  # 表单项标签
    labelRemark: Optional[str]  # 表单项标签描述
    description: Optional[str]  # 描述
    placeholder: Optional[str]  # 描述
    inline: bool = False  # 内联样式
    submitOnChange: bool = False  # 是否该表单项值发生变化时就提交当前表单。
    disabled: bool = False
    disableOn: Optional[str]  # 配置规则查看https://baidu.gitee.io/amis/docs/components/form/formitem
    visible: bool = True
    visibleOn: Optional[str]  # 配置规则查看https://baidu.gitee.io/amis/docs/components/form/formitem
    required: bool = True
    requiredOn: Optional[str]
    hidden: bool = False  # 可使用条件配置如 this.number>1
    hiddenOn: Optional[str]  # 配置判定逻辑
    validations: Optional[Dict[str, Union[int, str]]]  # 注意，键值对请参考ValidateEnum
    validationErrors: Optional[
        Dict[str, str]
    ]  # 注意，键值对请参考ValidateEnum，举例："minimum": "同学，最少输入$1以上的数字哈",其中$1为该错误的数据
    className: Optional[str]  # 表单最外层类名
    inputClassName: Optional[str]  # 表单控制器类名
    labelClassName: Optional[str]  # label 的类名
    mode: ItemModel = ItemModel.normal
    size: FormWidgetSize = FormWidgetSize.md
