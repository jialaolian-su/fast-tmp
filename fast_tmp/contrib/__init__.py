from typing import Type

from fast_tmp.models import AbstractUser, AbstractRole, AbstractPermission


# fixme:等待完成
def get_user_model() -> Type[AbstractUser]:
    return AbstractUser


def get_role_model() -> Type[AbstractRole]:
    return AbstractRole


def get_permission_model() -> Type[AbstractPermission]:
    return AbstractPermission
