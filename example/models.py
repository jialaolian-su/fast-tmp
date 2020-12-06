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
    name = fields.CharField(max_length=32)
    books: fields.ReverseRelation["Book"]


class Book(Model):
    name = fields.CharField(max_length=32)
    author: fields.ForeignKeyRelation[Author] = fields.ForeignKeyField("models.Author", related_name="books")


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
