from tortoise import fields, models


class AbstractModel(models.Model):
    created_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


from fast_tmp.utils.password import make_password, verify_password


class Permission(AbstractModel):
    name = fields.CharField(max_length=255)
    codename = fields.CharField(max_length=100)


class Group(AbstractModel):
    name = fields.CharField(max_length=150, unique=True)
    permissions = fields.ManyToManyField("models.Permission", related_name="groups")


# todo:测试是否有必要增加ManyToManyRelation字段
class User(AbstractModel):
    username = fields.CharField(
        max_length=150,
        unique=True,
    )
    nickname = fields.CharField(max_length=150)
    email = fields.CharField(
        max_length=255,
    )
    is_active = fields.BooleanField(
        default=True,
    )
    is_superuser = fields.BooleanField(default=False)
    password = fields.CharField(max_length=255)  # 设置密码
    salt = fields.CharField(max_length=32, description="随机盐")
    groups = fields.ManyToManyField("models.Group", related_name="users")
    permissions = fields.ManyToManyField("models.Permission")

    def set_password(self, raw_password: str):
        """
        设置密码
        :param raw_password:
        :return:
        """
        self.password, self.salt = make_password(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        """
        验证密码
        :param raw_password:
        :return:
        """
        return verify_password(raw_password, self.password, self.salt)
