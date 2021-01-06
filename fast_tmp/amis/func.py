from fastapi import Header


async def need_permission():
    pass


async def need_permission2(
    token: str = Header(
        ...,
    )
):
    print(token)
