from typing import Optional
from tortoise import QuerySet, Model


class PaginatorDepends(object):
    def __init__(self, queryset: QuerySet[Model], ):
        """
        应该在AdminType初始化的时候，直接把对应的queryset写入到init里面，这样在使用的时候直接用depends依赖该函数即可。
        :param queryset:
        :param limit:
        :param offset:
        """
        self.queryset = queryset

    def __call__(self, ) -> QuerySet[Model]:
        return self.queryset


class LimitOffsetPaginatorDepends(PaginatorDepends):
    """
    分页工具（其他实现方式未定）
    """

    def __init__(self, queryset: QuerySet[Model], limit: int = 10, offset: int = 0):
        """
        应该在AdminType初始化的时候，直接把对应的queryset写入到init里面，这样在使用的时候直接用depends依赖该函数即可。
        :param queryset:
        :param limit:
        :param offset:
        """
        super().__init__(queryset)
        self.limit = limit
        self.offset = offset

    def __call__(self, limit: Optional[int] = None,
                 offset: Optional[int] = None) -> QuerySet[Model]:
        if limit is not None and offset is not None:
            queryset = self.queryset.limit(limit).offset(offset)
        else:
            queryset = self.queryset.limit(self.limit).offset(self.offset)
        return queryset
