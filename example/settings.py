# -*- encoding: utf-8 -*-
"""
@File    : settings.py
@Time    : 2020/12/2 21:57
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""

import logging
import os
import sys

import sentry_sdk
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_SECRET = os.getenv("API_SECRET")
ADMIN_SECRET = os.getenv("ADMIN_SECRET")
if os.getenv("SENTRY_DSN"):  # 如果配置了sentry，则启动相关的服务
    from sentry_sdk.integrations.redis import RedisIntegration

    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        environment=os.getenv("ENVIRONMENT", "development"),
        integrations=[RedisIntegration()],
    )
DEBUG = os.getenv("DEBUG") == "True"
PROJECT_CODE = "AUDIT"

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", 3306)
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
SERVER_URL = os.getenv("SERVER_URL")

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": DB_HOST,
                "port": DB_PORT,
                "user": DB_USER,
                "password": DB_PASSWORD,
                "database": DB_NAME,
                "echo": os.getenv("DB_ECHO") == "True",
                "maxsize": 10,
            },
        },
    },
    "apps": {
        "models": {
            "models": ["example.models", "aerich.models","fast_tmp.models"],
            "default_connection": "default",
        },
    },
}

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

REDIS = {
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "password": REDIS_PASSWORD,
    "db": 2,
    "encoding": "utf-8",
}

REARQ = {
    "redis_host": REDIS_HOST,
    "redis_port": REDIS_PORT,
    "redis_password": REDIS_PASSWORD,
    "redis_db": 1,
}

# logging
LOGGER = logging.getLogger("example")
if DEBUG:
    LOGGER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
LOGGER.addHandler(sh)

SERVER_HOST = os.getenv("SERVER_HOST")