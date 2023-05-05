from fastapi import FastAPI
from blog.database import engine, Base
from blog.routers import blog, user, authentication

from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn


app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
Base.metadata.create_all(engine)


@app.on_event("startup")
async def on_startup_event():
    redis_cache = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")


if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=8000, app=app)

