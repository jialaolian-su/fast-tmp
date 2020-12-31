from tortoise.contrib.pydantic import pydantic_model_creator

from ..models import User

UserCreateSchema = pydantic_model_creator(
    User,
    exclude_readonly=True,
)
