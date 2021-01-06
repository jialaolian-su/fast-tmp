from typing import Any, Optional

from . import Control, ControlEnum


class SwitchItem(Control):
    type = ControlEnum.switch
    option: Optional[str]
    trueValue: Any = True
    falseValue: Any = False
