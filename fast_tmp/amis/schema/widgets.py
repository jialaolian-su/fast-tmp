from pydantic.main import BaseModel

from fast_tmp.amis.schema.enums import ControlEnum


class Column(BaseModel):
    """
    用于列表等的显示
    """

    name: str
    label: str


class Control(BaseModel):
    """
    用户form表单等写入
    """

    type: ControlEnum = ControlEnum.text  # 把这个和schema获取的参数进行融合，保证schema获取的值可以使用
    name: str
    label: str
