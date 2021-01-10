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
from typing import Optional
import sentry_sdk
# import sentry_sdk
import os
import dotenv
from sentry_sdk.integrations.redis import RedisIntegration

dotenv.load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL =os.getenv("DATABASE_URL")
DEBUG = os.getenv("DEBUG") == "True"
PROJECT_CODE = "AUDIT"
SECRET_KEY = "asdfadagre"


SERVER_URL = os.getenv("SERVER_URL")

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("ENVIRONMENT", "development"),
    integrations=[RedisIntegration()],
)



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
