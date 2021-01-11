from example.factory import create_app
app=create_app()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("example.main:app",debug=True, reload=True, lifespan="on" )
