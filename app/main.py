from fastapi import FastAPI
from blog.database import engine, Base
from blog.routers import blog, user, authentication, tasks
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from config import REDIS_HOST
import uvicorn


app = FastAPI(
    title="Blogs UA"
)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(tasks.router)
Base.metadata.create_all(engine)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.on_event("startup")
async def on_startup_event():
    redis_cache = aioredis.from_url(REDIS_HOST, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")
    print("Blyadina")


@app.on_event("shutdown")
async def on_shutdown_event():
    print("Perdun blyadun")


if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=8000, app=app)

