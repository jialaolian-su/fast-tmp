# -*- encoding: utf-8 -*-
"""
@File    : models.py
@Time    : 2020/12/2 22:22
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from tortoise.models import Model
from tortoise import fields


class Author(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=32)

    books: fields.ReverseRelation["Book"]

    class Meta:
        ordering = ["name"]


class Book(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=32)
    author: fields.ForeignKeyRelation[Author] = fields.ForeignKeyField("models.Author", related_name="books")

    class Meta:
        ordering = ["name"]


class Publish(Model):
    name = fields.CharField(max_length=32)
    books = fields.ManyToManyField("models.Book", related_name="publishs")


class School(Model):
    uuid = fields.UUIDField(pk=True)
    name = fields.TextField()
    id = fields.IntField(unique=True)

    students: fields.ReverseRelation["Student"]
    principal: fields.ReverseRelation["Principal"]


class Student(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    school: fields.ForeignKeyRelation[School] = fields.ForeignKeyField(
        "models.School", related_name="students", to_field="id"
    )


class Principal(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    school: fields.OneToOneRelation[School] = fields.OneToOneField(
        "models.School", on_delete=fields.CASCADE, related_name="principal", to_field="id"
    )


class Tournament(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    events: fields.ReverseRelation["Event"]

    class Meta:
        ordering = ["name"]


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    tournament: fields.ForeignKeyNullableRelation[Tournament] = fields.ForeignKeyField(
        "models.Tournament", related_name="events", null=True
    )
    participants: fields.ManyToManyRelation["Team"] = fields.ManyToManyField(
        "models.Team", related_name="events", through="event_team"
    )
    address: fields.OneToOneNullableRelation["Address"]

    class Meta:
        ordering = ["name"]


class Address(Model):
    city = fields.CharField(max_length=64)
    street = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)

    event: fields.OneToOneRelation[Event] = fields.OneToOneField(
        "models.Event", on_delete=fields.CASCADE, related_name="address", pk=True
    )

    class Meta:
        ordering = ["city"]


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    events: fields.ManyToManyRelation[Event]

    class Meta:
        ordering = ["name"]


from fast_tmp.models import AbstractUser, AbstractPermission, AbstractRole, AbstractAdminLog


class User(AbstractUser):
    pass


class Permission(AbstractPermission):
    pass


class Role(AbstractRole):
    pass


class AdminLog(AbstractAdminLog):
    pass
