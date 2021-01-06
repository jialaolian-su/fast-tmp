import json
from datetime import datetime
from typing import Optional, Type

from fastapi import Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from starlette.requests import Request

from fast_tmp.amis_router import AmisRouter
from fast_tmp.conf import settings
from fast_tmp.core.mixins import AimsListMixin
from fast_tmp.models import User
from fast_tmp.schema import UserCreateSchema
from fast_tmp.templates_app import templates
from fast_tmp.utils.model import get_model_from_str

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.EXPIRES_DELTA
User: User = get_model_from_str(settings.AUTH_USER_MODEL)


class AccessTokenInfo(BaseModel):
    username: str
    login_at: datetime
    scope: Optional[str]


class UserSchema(BaseModel):
    username: str
    is_active: Optional[bool] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

auth_router = AmisRouter(prefix="/auth")


async def get_user(username: str) -> Optional[User]:
    user = await User.filter(username=username).first()
    return user


async def authenticate_user(username: str, password: str) -> Optional[User]:
    user = await get_user(username)
    if not user:
        return None
    if not user.verify_password(password):
        return None
    return user


def encode_jwt(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def create_access_token(data: AccessTokenInfo):
    to_encode = data.dict()
    expire = datetime.utcnow() + settings.EXPIRES_DELTA
    to_encode.update({"exp": expire})
    encoded_jwt = encode_jwt(to_encode)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user: User = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data=AccessTokenInfo(username=user.username, login_at=datetime.now()),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/users/me/", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@auth_router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@auth_router.post("/users", response_model=UserCreateSchema)
async def create_user(user: UserCreateSchema):
    u = User(**user.dict())
    u.set_password(user.password)
    await u.save()
    return u


x = AimsListMixin(
    path="/list",
    search_classes=("name",),
    model_str="User",
    app_label="models",
    exclude=["groups"],
)
x.init(auth_router)


@auth_router.get("/template", response_class=HTMLResponse)
async def template(
    request: Request,
):
    return templates.TemplateResponse(
        "admin/crud.html", {"request": request, "page": str(json.dumps(page))}
    )


@auth_router.get("/template2", response_class=HTMLResponse)
async def template(
    request: Request,
):
    return templates.TemplateResponse(
        "admin/t.html",
        {
            "request": request,
        },
    )


@auth_router.get("/index", response_class=HTMLResponse)
async def index(
    request: Request,
):
    return templates.TemplateResponse(
        "admin/index.html",
        {
            "request": request,
        },
    )
