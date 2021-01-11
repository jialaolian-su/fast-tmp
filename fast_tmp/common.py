from enum import Enum
from typing import List, Optional, Type

from pydantic import BaseModel


class MethodTYpe(str, Enum):
    html = "html"
    get = "get"
    post = "post"


class PermissionTree(BaseModel):
    name: str
    label: str
    id: str
    need_perm: bool
    prefix: str
    children: List[Type["PermissionTree"]] = []
    type: MethodTYpe
    codename: str
    parent_codename: Optional[str]


# class PermissionManage():
#     permissiontrees: List[PermissionTree] = []
#     need_father_permissions: List[PermissionTree] = []
#
#     def add_permission(self, pt: PermissionTree, father_pt: Optional[PermissionTree] = None):
#         if not father_pt:
#             if pt.parent_codename:
#                 for permission in self.permissiontrees:
#                     if permission.codename == pt.parent_codename:
#                         permission.children.append(pt)
#                         break
#         else:
#             for permission in self.permissiontrees:
#                 if permission.codename == father_pt.codename:
#                     permission.children.append(pt)
#                     break
#             else:
#                 pass
#                 # self.add_permission(father_pt)
#         self.permissiontrees.append(pt)
SITE = {}
