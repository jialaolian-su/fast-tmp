# -*- encoding: utf-8 -*-
"""
@File    : db.py
@Time    : 2021/1/8 21:43
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from sqlalchemy.orm import sessionmaker

from fast_tmp.conf import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    settings.DATABASE_URL, echo=True, future=True
)
SessionLocal = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine
)