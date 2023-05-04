from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from .blog.database import engine, Base
from .blog.routers import blog, user, base
from time import time
import uvicorn


app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(base.router)

Base.metadata.create_all(engine)

templates = Jinja2Templates(directory="templates")


@app.middleware('http')
async def process_time_middleware(request: Request, call_next):
    start = time()
    response = await call_next(request)
    print(round(time() - start, 5))
    return response


@app.get('/')
async def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("index.html", context)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

