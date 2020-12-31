from datetime import datetime
from typing import Optional, Type

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from fast_tmp.conf import settings
from fast_tmp.models import AbstractUser
from fast_tmp.utils.model import get_model_from_str

User: AbstractUser = get_model_from_str(settings.AUTH_USER_MODEL)  # noqa


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# todo:重构

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user(username: str):
    User = get_model_from_str("User")
    user = await User.filter(username=username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


# fixme:修复返回类型


def authenticate_user(username: str, password: str):
    """
    要求有登录
    """
    user = await get_user(username)
    if not user.verify_password(password) or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


class TokenInfo(BaseModel):
    username: str
    scope: Optional[str]


def create_token(data: TokenInfo):
    to_encode = data.copy()
    expire = datetime.utcnow() + settings.EXPIRES_DELTA
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def parse_token(token: str) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


async def get_current_user(token: str = Depends(oauth2_scheme)):
    username = parse_token(token)
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
