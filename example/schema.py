from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from fast_tmp.models import User

PydanticUser = sqlalchemy_to_pydantic(User)


class Token(BaseModel):
    access_token: str
    token_type: str
