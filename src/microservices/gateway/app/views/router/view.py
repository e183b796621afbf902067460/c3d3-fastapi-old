from fastapi import FastAPI

from app.views.auth.view import app as auth_app
from app.views.с3.view import app as c3_app
from app.views.d3.view import app as d3_app


app = FastAPI()

app.include_router(router=auth_app)
app.include_router(router=c3_app)
app.include_router(router=d3_app)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='view:app', host='0.0.0.0')

