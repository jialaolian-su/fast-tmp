from typing import Type

from tortoise import fields, models

from fast_tmp.utils.password import make_password, verify_password


class AbstractUser(models.Model):
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=200, )
    is_active = fields.BooleanField(default=True, )
    is_superuser = fields.BooleanField(default=False)

    class Meta:
        abstract = True

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

    def __str__(self):
        return self.username


class AbstractPermission(models.Model):
    label = fields.CharField(max_length=128)
    model = fields.CharField(max_length=128)
    codename = fields.CharField(max_length=128)

    def __str__(self):
        return self.label

    class Meta:
        abstract = True

    @classmethod
    def make_permission(cls, model: Type[models.Model], ):
        """
        生成model对应的权限
        """
        # todo:生成对应默认权限


class AbstractRole(models.Model):
    label = fields.CharField(max_length=50)
    users: fields.ManyToManyRelation[AbstractUser] = fields.ManyToManyField("models.User")
    permissions: fields.ManyToManyRelation[AbstractPermission] = fields.ManyToManyField("models.Permission")

    def __str__(self):
        return self.label

    class Meta:
        abstract = True


class AbstractAdminLog(models.Model):
    admin = fields.ForeignKeyField("models.User")
    action = fields.CharField(max_length=20)
    model = fields.CharField(max_length=50)
    content = fields.JSONField()

    class Meta:
        abstract = True
