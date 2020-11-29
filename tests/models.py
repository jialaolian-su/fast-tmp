import datetime
from enum import IntEnum

from tortoise import fields

from fast_tmp.models import AbstractModel


class ProductType(IntEnum):
    article = 1
    page = 2


class PermissionAction(IntEnum):
    create = 1
    delete = 2
    update = 3
    read = 4


class Status(IntEnum):
    on = 1
    off = 0


class Email(AbstractModel):
    email = fields.CharField(max_length=200)
    is_primary = fields.BooleanField(default=False)
    user = fields.ForeignKeyField("models.User", db_constraint=False)


class Category(AbstractModel):
    slug = fields.CharField(max_length=200)
    name = fields.CharField(max_length=200)
    user = fields.ForeignKeyField("models.User", description="User")
    created_at = fields.DatetimeField(auto_now_add=True)


class Product(AbstractModel):
    categories = fields.ManyToManyField("models.Category")
    name = fields.CharField(max_length=50)
    view_num = fields.IntField(description="View Num")
    sort = fields.IntField()
    is_reviewed = fields.BooleanField(description="Is Reviewed")
    type = fields.IntEnumField(ProductType, description="Product Type")
    image = fields.CharField(max_length=200)
    body = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)


class Config(AbstractModel):
    label = fields.CharField(max_length=200)
    key = fields.CharField(max_length=20)
    value = fields.JSONField()
    status: Status = fields.IntEnumField(Status, default=Status.on)
