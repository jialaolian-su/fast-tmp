from typing import Type

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from fast_tmp.utils.password import make_password, verify_password

Base = declarative_base()


class ControlSer(BaseModel):
    label: str
    name: str
    type: str


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, info={"kwargs": "ddd"})
    username = Column(String(128), unique=True)
    password = Column(
        String(200),
    )
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=True)

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


class Permission(Base):
    __tablename__ = "permission"
    id = Column(Integer, primary_key=True)
    label = Column(String(128))
    codename = Column(String(128), unique=True)
    parent_codename = Column(String(128), unique=True)

    def __str__(self):
        return self.label

    @classmethod
    def make_permission(
        cls,
        model: Type[Base],
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


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    label = Column(
        String(128),
    )

    users = relationship(
        "User",
        secondary=Table(
            "group_user",
            Base.metadata,
            Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
            Column("group_id", Integer, ForeignKey("group.id"), primary_key=True),
        ),
        backref="groups",
    )
    permissions = relationship(
        "Permission",
        secondary=Table(
            "group_permission",
            Base.metadata,
            Column("group_id", Integer, ForeignKey("group.id"), primary_key=True),
            Column("permission_id", Integer, ForeignKey("permission.id"), primary_key=True),
        ),
        backref="permisions",
    )

    def __str__(self):
        return self.label


class AdminLog(Base):
    __tablename__ = "adminlog"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
