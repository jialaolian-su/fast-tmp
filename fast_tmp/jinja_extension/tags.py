import jinja2
from pydantic import typing

from fast_tmp.conf import settings


def register_tags(templates):
    env = templates.env

    @jinja2.contextfunction
    def static(context: dict, **path_params: typing.Any) -> str:
        request = context["request"]
        path = settings.STATIC_URL
        return request.url_for(path, **path_params)

    env.globals["static"] = static
