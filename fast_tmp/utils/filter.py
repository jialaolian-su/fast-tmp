from typing import Optional


class Filter:
    creation_counter = 0

    # field_class = forms.Field #???
    def __init__(self, field_name: Optional[str] = None, lookup_expr: Optional[str] = None, *, label):
        pass


class FilterSetMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['declared_filters'] = cls.get_declared_filters(bases, attrs)

    @classmethod
    def get_declared_filters(cls, bases, attrs):
        filters = [
            (filter_name, attrs.pop(filter_name))
            for filter_name, obj in attrs.items() if isinstance(obj, Filter)
        ]
