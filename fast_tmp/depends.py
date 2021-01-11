from datetime import datetime
from typing import Optional, Type, List

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError

from fast_tmp.conf import settings
from fast_tmp.utils.model import get_model_from_str

User: AbstractUser = get_model_from_str(settings.AUTH_USER_MODEL)  # noqa


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


async def get_current_user(
        security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_user_or_none(security_scopes: SecurityScopes, token: Optional[str] = Depends(oauth2_scheme)):
    pass


async def get_current_active_user(current_user: User = Security(get_current_user, scopes=[])):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_site(user: User = Depends(get_current_active_user)):
