from enum import Enum


class Method(str, Enum):
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    PUT = 'PUT'


class ElementType(str, Enum):
    Button = 'Button'
    Grid = 'Grid'
    Form = 'Form'
    Null = 'Null'
