from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
import jwt
from users.utills import UserUtills, get_user_utills


async def token_validator(request: Request, call_next):
    utills = get_user_utills()
    headers = request.headers
    cookies = request.cookies
    url = request.url.path
    docs_whitelist = ('/docs', 'redoc')
    user_whitelist = ('/users/signup', '/users/login')
    post_whitelist = ('/posts/')

    if url.startswith(('/posts', '/users')):
        if url.startswith(user_whitelist) | (url.startswith(post_whitelist) and request.method == 'GET') | (url.startswith(docs_whitelist)):
            response = await call_next(request)
            return response
    
        if "access_token" in cookies.keys():
            access_token = cookies.get('access_token')
            access_token = access_token.replace("Bearer ", "")
            decoded_token = decode_token(access_token)
            request.state.user = decoded_token['data']
            response = await call_next(request)
            return response
        return JSONResponse({'detail': 'Token is required'}, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        response = await call_next(request)
        return response
    

def decode_token(token):
    JWT_SECRET_KEY = 'test'
    JWT_ALGORITHM = 'HS256'

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.exceptions.InvalidTokenError as e:
        e.args = ['Invalid token']
        return e