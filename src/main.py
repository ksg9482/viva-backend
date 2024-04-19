from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTask

import logging
from starlette.middleware.base import BaseHTTPMiddleware #세션 관리

# jwt
from auth.middlewares import token_validator
from database import Base, engine
from contextlib import asynccontextmanager
from users import routers as user_router
from posts import routers as post_router
import uvicorn

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # dev일때만. 실제로는 사용하면 안됨
        await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)
    yield 

logging.basicConfig(filename='info.log', level=logging.DEBUG)
def log_info(req_body, res_body):
    logging.info(req_body)
    logging.info(res_body)



app = FastAPI(
    lifespan=app_lifespan, 
    # docs_url=None, 
    # redoc_url=None
    ) 

def custom_logger(request: Request, response: JSONResponse, logger: logging.Logger = Depends()):
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Response: {response.status_code}")
    return response

app.include_router(user_router.router)
app.include_router(post_router.router)

app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=token_validator)
# @app.middleware('http')
# async def some_middleware(request: Request, call_next):
#     req_body = await request.body()
#     response = await call_next(request)

#     res_body = b''
#     async for chunk in response.body_iterator:
#         res_body += chunk

#     task = BackgroundTask(log_info, req_body, res_body)
#     return Response(content=res_body, status_code=response.status_code,
#                     headers=dict(response.headers), media_type=response.media_type, background=task)



# logger = logging.getLogger("uvicorn")
# logger.setLevel(logging.INFO)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8083, reload=True, reload_dirs=["src"])
