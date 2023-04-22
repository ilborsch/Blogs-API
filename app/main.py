from fastapi import FastAPI
from blog.database import engine, Base
from blog.routers import blog, user, authentication
import uvicorn


app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
Base.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=8000, app=app)

