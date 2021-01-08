from sqlalchemy import select
from sqlalchemy.orm import selectinload, subqueryload, joinedload, sessionmaker

from example.db import SessionLocal
from fast_tmp.models import User
from sqlalchemy.future import select

from example.factory import create_app
app=create_app()


@app.get("/test")
async def test():
    # raise Exception("test fast-tmp")
    async with SessionLocal() as session:
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
    async with SessionLocal() as session:
        session.add_all([u1, u2])
        await session.commit()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, )
