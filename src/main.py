from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from src.auth.middlewares import token_validator
from src.database import Base, engine
from src.auth import routers as auth_router
from src.users import routers as user_router
from src.posts import routers as post_router
import uvicorn

async def app_lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # dev일때만. 실제로는 사용하면 안됨
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield 

app = FastAPI(
    lifespan=app_lifespan, 
    # docs_url=None, 
    # redoc_url=None
    ) 

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(post_router.router)

app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=token_validator)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8083, reload=True, reload_dirs=["src"])