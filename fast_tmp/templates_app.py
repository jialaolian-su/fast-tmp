import os
import sys

from fastapi.templating import Jinja2Templates

from fast_tmp.jinja_extension.tags import register_tags

paths = sys.path


def get_dir():
    return os.path.dirname(__file__)


DIR = get_dir()

template_path = os.path.join(DIR, "templates")
templates = Jinja2Templates(directory=template_path)
register_tags(templates)
