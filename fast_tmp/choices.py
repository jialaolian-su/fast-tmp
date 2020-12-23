from enum import Enum


class Method(str, Enum):
    GET = 'GET'
    POST = 'POST'


class ElementType(str, Enum):
    Button = 'Button'
    Grid = 'Grid'
    Form = 'Form'
    Null = 'Null'
