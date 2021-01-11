from sqlalchemy import select
from sqlalchemy.orm import selectinload, subqueryload, joinedload

from fast_tmp.models import User

from example.factory import create_app
app=create_app()


@app.get("/test")
async def test():
    # raise Exception("test fast-tmp")
   pass


@app.post("/test")
async def test_create():
    pass


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, )
