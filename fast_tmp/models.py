from typing import Type

from pydantic import BaseModel
from tortoise import Model, fields

from fast_tmp.utils.password import make_password, verify_password


class Permission(Model):
    label = fields.CharField(max_length=128)
    codename = fields.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.label

    @classmethod
    def make_permission(
        cls,
        model: Type[BaseModel],
    ):
        """
        生成model对应的权限
        """
        model_name = model.__name__
        Permission.get_or_create(
            defaults={
                "label": "can read " + model_name,
                "model": model_name,
                "codename": "can_read_" + model_name,
            }
        )
        Permission.get_or_create(
            defaults={
                "label": "can create " + model_name,
                "model": model_name,
                "codename": "can_create_" + model_name,
            }
        )
        Permission.get_or_create(
            defaults={
                "label": "can update " + model_name,
                "model": model_name,
                "codename": "can_update_" + model_name,
            }
        )
        Permission.get_or_create(
            defaults={
                "label": "can delete " + model_name,
                "model": model_name,
                "codename": "can_delete_" + model_name,
            }
        )


class User(Model):
    username = fields.CharField(max_length=128)
    password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    # groups = fields.ManyToManyField("fast_tmp.Group", related_name='users')

    def set_password(self, raw_password: str):
        """
        设置密码
        :param raw_password:
        :return:
        """
        self.password = make_password(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        """
        验证密码
        :param raw_password:
        :return:
        """
        return verify_password(raw_password, self.password)

    def has_perm(self, perm: "Permission"):
        """
        判定用户是否有权限
        """
        pass

    async def get_perms(self):
        permissions = await Permission.filter(groups__users=self.pk)
        return permissions

    def __str__(self):
        return self.username


class Group(Model):
    label = fields.CharField(max_length=128)
    permissions = fields.ManyToManyField("fast_tmp.Permission", related_name="groups")
    users = fields.ManyToManyField("fast_tmp.User", related_name="groups")

    def __str__(self):
        return self.label


class Config(Model):
    name = fields.CharField(max_length=64)
    key = fields.CharField(max_length=64, unique=True)
    value = fields.JSONField()
