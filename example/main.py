# -*- encoding: utf-8 -*-
"""
@File    : main.py
@Time    : 2020/12/2 21:57
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import uvicorn

from example import settings
from example.factory import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "example.main:app", host="0.0.0.0", port=8000, debug=settings.DEBUG, reload=settings.DEBUG, lifespan="on"
    )
