from typing import Iterator, Type, TypeVar

from tortoise import Model, Tortoise

TModel = TypeVar("TModel", bound=Model)


def get_all_models() -> Iterator[TModel]:
    """
    get all tortoise models
    :return:
    """
    for tortoise_app, models in Tortoise.apps.items():
        for model_item in models.items():
            yield model_item


def get_model_from_str(model_name: str, app_label: str = "models") -> Type[TModel]:
    s = model_name.split(".")
    if len(s) == 2:
        app_label, model_name = s
    for tortoise_app, models in Tortoise.apps.items():
        if tortoise_app == app_label:
            for name, model in models.items():
                if model_name == name:
                    return model
    else:
        raise Exception(f"Can not found {model_name}!")
