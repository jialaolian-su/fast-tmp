from typing import List, Type, Union

from pydantic import BaseModel
from tortoise import Model, fields

from fast_tmp.utils.password import make_password, verify_password


class Permission(Model):
    label = fields.CharField(max_length=128)
    codename = fields.CharField(max_length=128, unique=True)

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

    def __eq__(self, other) -> bool:
        if other == self.codename or getattr(other, "codename", None) == self.codename:
            return True
        return False

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label


class User(Model):
    username = fields.CharField(max_length=128, unique=True)
    password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    groups: fields.ManyToManyRelation["Group"]

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

    @property
    async def perms(self):
        if not hasattr(self, "__perms"):
            permission_instances = await Permission.filter(groups__users=self.pk)
            self.__perms = permission_instances
        return self.__perms

    async def has_perm(self, perm: Union[Permission, str]) -> bool:
        """
        判定用户是否有权限
        """
        if self.is_superuser:
            return True
        for permission_instance in self.perms:
            if permission_instance == perm:
                return True
        return False

    async def has_perms(self, perms: List[Union[Permission, str]]) -> bool:
        """
        根据permission的codename进行判定
        """
        if self.is_superuser:
            return True
        for perm in perms:
            for perm_instance in self.perms:
                if perm == perm_instance.codename:
                    continue
            else:
                return False
        return True

    async def get_perms(self):
        return self.perms

    def __str__(self):
        return self.username


class Group(Model):
    label = fields.CharField(max_length=128, unique=True)
    permissions = fields.ManyToManyField("fast_tmp.Permission", related_name="groups")
    users = fields.ManyToManyField("fast_tmp.User", related_name="groups")

    def __str__(self):
        return self.label


class Config(Model):
    name = fields.CharField(max_length=64)
    key = fields.CharField(max_length=64, unique=True)
    value = fields.JSONField()
