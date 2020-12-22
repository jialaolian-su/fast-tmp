from typing import Type

from tortoise import Tortoise, Model


def get_all_models():
    """
    get all tortoise models
    :return:
    """
    for tortoise_app, models in Tortoise.apps.items():
        for model_item in models.items():
            yield model_item


def get_model_from_str(model_name: str) -> Type[Model]:
    for tortoise_app, models in Tortoise.apps.items():
        for name, model in models.items():
            if model_name == name:
                return model
        else:
            raise Exception("未找到对象")
