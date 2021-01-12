from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request

from fast_tmp.amis.schema.app import AppSchema
from fast_tmp.amis_router import AmisRouter
from fast_tmp.api.admin import get_site_from_permissionschema, init_permission
from fast_tmp.conf import settings
from fast_tmp.depends import authenticate_user, get_current_user
from fast_tmp.models import Permission, User
from fast_tmp.templates_app import templates
from fast_tmp.utils.token import create_access_token

router = AmisRouter(prefix="/base")
INIT_PERMISSION = False


@router.get("/site")
async def get_site(user: User = Depends(get_current_user)):
    """
    获取左侧导航栏
    :param user:
    :return:
    """
    global INIT_PERMISSION
    from example.main import app

    # 初始化permission
    if not INIT_PERMISSION:
        await init_permission(app.site_schema, list(await Permission.all()))
        INIT_PERMISSION = True
    permissions = await user.perms
    site = get_site_from_permissionschema(app.site_schema, permissions, settings.SERVER_URL, user)
    return site


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.EXPIRES_DELTA


@router.get("/index")
async def index(request: Request, username: str, password: str):
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = ACCESS_TOKEN_EXPIRE_MINUTES
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    data = {"access_token": access_token, "token_type": "bearer"}
    global INIT_PERMISSION
    from example.main import app

    # 初始化permission
    if not INIT_PERMISSION:
        await init_permission(app.site_schema, list(await Permission.all()))
        INIT_PERMISSION = True
    permissions = await user.perms
    x = get_site_from_permissionschema(app.site_schema, permissions, "", user)
    page = AppSchema(
        brandName="项目测试",
        pages=[get_site_from_permissionschema(app.site_schema, permissions, "", user)],
        data=data,
    )
    return templates.TemplateResponse(
        "admin/index.html",
        {"request": request, "page": page.json(), "access_token": access_token},
    )
