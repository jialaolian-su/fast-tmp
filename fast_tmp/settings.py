# 需要能够读取项目的settings
import importlib
import os

# todo:app的settings路径要写入环境变量
print(os.getenv("settings_path"))
app_settings = importlib.import_module(os.getenv("SETTINGS_MODULE"))

REDIS_HOST = getattr(app_settings, "REDIS_HOST", None) or "localhost"
REDIS_PORT = getattr(app_settings, "REDIS_PORT", None) or "6379"
REDIS_DB = getattr(app_settings, "REDIS_DB", None) or 1
REDIS_PASSWORD = getattr(app_settings, "REDIS_PASSWORD", None) or None
