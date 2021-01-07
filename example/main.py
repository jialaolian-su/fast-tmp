import databases
from fastapi import FastAPI
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload, subqueryload, joinedload

from fast_tmp.conf import settings
from fast_tmp.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select

app = FastAPI()
print(settings.DATABASE_URL)
engine = create_async_engine(
    settings.DATABASE_URL, echo=True, future=True
)
session = AsyncSession(engine, future=True)


# database = databases.Database("postgresql://dbuser:shiguang123@localhost/fast_tmp")


@app.on_event("startup")
async def startup():
    await session.begin()
    # await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await session.close_all()
    # await database.disconnect()


# @app.get("/test")
# async def test():
#     query = select(User)
#     await database.execute(query)


@app.get("/test")
async def test():
    query1 = select(User).options(selectinload(User.groups))
    query2 = select(User).options(subqueryload(User.groups))
    query3 = select(User).options(joinedload(User.groups))
    users = await session.execute(query1)
    for user in users:
        print(user)
    users = await session.execute(query2)
    for user in users:
        print(user)
    users = await session.execute(query3)
    for user in users:
        print(user)


@app.post("/test")
async def test_create():
    u1 = User(username="user1")
    u1.set_password("user1")
    u2 = User(username="user2")
    u2.set_password("user1")
    session.add_all([u1, u2])
    await session.commit()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, )
