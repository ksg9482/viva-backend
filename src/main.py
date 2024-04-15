from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware #세션 관리
# jwt
from database import Base, engine
from contextlib import asynccontextmanager
from users.routers import router as user_router
from posts.routers import router as post_router
import uvicorn

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with engine.begin() as conn:
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
