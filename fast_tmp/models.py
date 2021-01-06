from typing import Type

from tortoise import fields, models

from fast_tmp.conf import settings
from fast_tmp.utils.password import make_password, verify_password


class User(models.Model):
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(
        max_length=200,
    )
    is_active = fields.BooleanField(
        default=True,
    )
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

    def has_perm(self, perm: "Permission"):
        """
        判定用户是否有权限
        """
        pass

    def __str__(self):
        return self.username

    # class Meta:
    #     abstract = True


# class User(AbstractUser):
#     pass


class Permission(models.Model):
    label = fields.CharField(max_length=128)
    model = fields.CharField(max_length=128)
    codename = fields.CharField(max_length=128, unique=True)
    groups: fields.ManyToManyRelation["Group"]

    def __str__(self):
        return self.label

    @classmethod
    def make_permission(
        cls,
        model: Type[models.Model],
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


class Group(models.Model):
    label = fields.CharField(max_length=50)
    users = fields.ManyToManyField("models.User")
    permissions = fields.ManyToManyField("models.Permission")

    def __str__(self):
        return self.label
