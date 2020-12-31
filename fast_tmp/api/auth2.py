from pydantic import BaseModel
from pydantic.schema import schema
from tortoise.contrib.pydantic import pydantic_queryset_creator

from fast_tmp.amis.schema.crud import CRUD
from fast_tmp.amis.utils import get_coulmns_from_pqc
from fast_tmp.conf import settings
from fast_tmp.core.amis_router import AmisRouter
from fast_tmp.utils.model import get_model_from_str

User = get_model_from_str(settings.AUTH_USER_MODEL)
auth2_router = AmisRouter(prefix="/admin2")
users_schema = pydantic_queryset_creator(User)


class A(BaseModel):
    items: users_schema
    total: int


@auth2_router.get(
    "/users",
    view=CRUD(
        api=settings.SERVER_URL + settings.ADMIN_URL + auth2_router.prefix + "/users",
        columns=get_coulmns_from_pqc(
            users_schema,
        ),
    ),
    response_model=A,
)
async def users():
    return {
        "total": await User.all().count(),
        "items": await users_schema.from_queryset(User.all()),
    }
