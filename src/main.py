from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware #세션 관리
# jwt
from database import Base, engine
from contextlib import asynccontextmanager
from users.routers import router as user_router
from users.models import User
from posts.routers import router as post_router
from posts.models import Post#, PostView 
import uvicorn

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # dev일때만. 실제로는 사용하면 안됨
        # await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)
    yield 

app = FastAPI(
    lifespan=app_lifespan, 
    # docs_url=None, 
    # redoc_url=None
    ) 

app.include_router(user_router)
app.include_router(post_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, reload_dirs=["src"])
