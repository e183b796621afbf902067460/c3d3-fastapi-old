from fastapi import FastAPI

from app.views.auth.view import app as auth_app


app = FastAPI()

app.include_router(router=auth_app)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='view:app', host='0.0.0.0')

