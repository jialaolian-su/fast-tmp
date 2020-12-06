import collections.abc
import inspect
import warnings
from math import ceil

from cache.cache import cached_property


class UnorderedObjectListWarning(RuntimeWarning):
    pass


class InvalidPage(Exception):
    pass


class PageNotAnInteger(InvalidPage):
    pass


class EmptyPage(InvalidPage):
    pass


class Paginator:
    pass


class LimitOffsetPaginator(Paginator):
    """
    分页工具
    """
    pass
