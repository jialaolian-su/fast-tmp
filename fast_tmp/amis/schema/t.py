from fast_tmp.amis.schema.forms.widgets import Column

from .amislist import AmisList
from .crud import CRUD

x = AmisList(
    body=CRUD(
        api="https://houtai.baidu.com/api/sample",
        columns=[
            Column(name="id", label="ID"),
            Column(name="engine", label="Rendering engine"),
            Column(name="browser", label="Browser"),
            Column(name="platform", label="Platform(s)"),
            Column(name="version", label="Engine version"),
            Column(name="grade", label="CSS grade"),
        ],
    )
)
