from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.auth.utills import JwtUtils


async def token_validator(request: Request, call_next):
    utills = JwtUtils()

    cookies = request.cookies
    url = request.url.path
    docs_whitelist = ('/docs', 'redoc')
    post_whitelist = ('/posts')

    # /posts, /users로 시작하는 url에 대해서만 토큰 검증
    if url.startswith(('/posts', '/users')):
        # /posts에 한해 GET 요청에 대해서는 토큰 검증을 하지 않음
        # /docs에 대해서도 토큰 검증을 하지 않음
        if (url.startswith(post_whitelist) and request.method == 'GET') | (url.startswith(docs_whitelist)):
            response = await call_next(request)
            return response
    
        if "access_token" in cookies.keys():
            access_token = cookies.get('access_token')
            access_token = access_token.replace("Bearer ", "")
            decoded_token = utills.decode_token(access_token)
            request.state.user = decoded_token['data']
            response = await call_next(request)
            return response
        return JSONResponse({'detail': 'Token is required'}, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        response = await call_next(request)
        return response