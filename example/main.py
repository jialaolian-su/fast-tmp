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
