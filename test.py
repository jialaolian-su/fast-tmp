from tortoise.contrib.pydantic import pydantic_model_creator

from fast_tmp.models import User,Group

x = pydantic_model_creator(User, exclude_readonly=True)
y= pydantic_model_creator(User,)
a = pydantic_model_creator(Group, exclude_readonly=True)
b= pydantic_model_creator(Group,)