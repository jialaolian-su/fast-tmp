# -*- encoding: utf-8 -*-
"""
@File    : settings.py
@Time    : 2020/12/20 23:34
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from dotenv import load_dotenv

FASTAPI_VARIABLE = "FASTAPI_SETTINGS_MODULE"


class Settings:
    def __init__(self, settings_module):
        settings_module = os.environ.get(FASTAPI_VARIABLE)
        if not settings_module:
            desc = ("setting %s" % name) if name else "settings"
            raise ImproperlyConfigured(
                "Requested %s, but settings are not configured. "
                "You must either define the environment variable %s "
                "or call settings.configure() before accessing settings."
                % (desc, FASTAPI_VARIABLE))
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        # store the settings module in case someone later cares
        self.SETTINGS_MODULE = settings_module

        mod = importlib.import_module(self.SETTINGS_MODULE)
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)
        if not self.SECRET_KEY:
            raise ImproperlyConfigured("The SECRET_KEY setting must not be empty.")
        # todo:时间处理


settings = Settings()
