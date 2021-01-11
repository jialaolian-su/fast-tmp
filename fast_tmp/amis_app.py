from typing import Any, Callable, ClassVar, Coroutine, Dict, List, Optional, Sequence, Type, Union

from fastapi import FastAPI
from fastapi.datastructures import Default
from fastapi.params import Depends
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute

from fast_tmp.amis_router import AmisRouter
from fast_tmp.common import SITE
from fast_tmp.utils.model import get_model_from_str


class AmisAPI(FastAPI):
    permissions: ClassVar[Dict[str, bool]] = {}

    def __init__(
        self,
        *,
        debug: bool = False,
        routes: Optional[List[BaseRoute]] = None,
        title: str = "FastAPI",
        description: str = "",
        version: str = "0.1.0",
        openapi_url: Optional[str] = "/openapi.json",
        openapi_tags: Optional[List[Dict[str, Any]]] = None,
        servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        docs_url: Optional[str] = "/docs",
        redoc_url: Optional[str] = "/redoc",
        swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect",
        swagger_ui_init_oauth: Optional[Dict[str, Any]] = None,
        middleware: Optional[Sequence[Middleware]] = None,
        exception_handlers: Optional[
            Dict[
                Union[int, Type[Exception]],
                Callable[[Request, Any], Coroutine[Any, Any, Response]],
            ]
        ] = None,
        on_startup: Optional[Sequence[Callable[[], Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
        openapi_prefix: str = "",
        root_path: str = "",
        root_path_in_servers: bool = True,
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
        **extra: Any,
    ) -> None:
        super().__init__(**locals())

    def include_router(
        self,
        router: AmisRouter,
        *,
        prefix: str = "",
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
        default_response_class: Type[Response] = Default(JSONResponse),
        callbacks: Optional[List[BaseRoute]] = None,
    ) -> None:
        AmisAPI.permissions.update(router.permissions)
        self.router.include_router(
            router,
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            responses=responses,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            default_response_class=default_response_class,
            callbacks=callbacks,
        )

    async def registe_permission(self):
        Permission = get_model_from_str("Permission")
        for k, v in AmisAPI.permissions.items():
            await Permission.get_or_create(
                codename=k, defaults={"model": v, "label": k.replace("_", " ")}
            )
