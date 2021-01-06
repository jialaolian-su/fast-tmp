from typing import Any, ClassVar, Dict, List, Optional, Sequence, Type, Union

from fastapi import FastAPI
from fastapi.datastructures import Default
from fastapi.params import Depends
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute

from fast_tmp.amis_router import AmisRouter
from fast_tmp.utils.model import get_model_from_str


class AmisAPI(FastAPI):
    permissions: ClassVar[Dict[str, bool]] = {}

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
