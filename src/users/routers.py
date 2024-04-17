from fastapi import APIRouter, Depends, HTTPException, Request, Response, logger

from users.schemas import UserEdit, UserEditResponse, UserLogin, UserLoginResponse, UserSignUp, UserSignUpResponse
from users.services import UserService, get_user_service

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

router = APIRouter(prefix='/users', tags=['users'])
# service: UserService = Depends(get_user_service)

@router.post('/signup', response_model=UserSignUpResponse,tags=['users'])
async def signup(signup_user: UserSignUp, service: UserService = Depends(get_user_service)):
    created_user = await service.create_user_account(username=signup_user.username, email=signup_user.email, password=signup_user.password)
    return created_user

@router.post('/login', response_model=UserLoginResponse, tags=['users'])
async def login(response:Response, user_login:UserLogin, service: UserService = Depends(get_user_service)):
    login_tokens = await service.login(user_login.email, user_login.password)

    response.set_cookie(key="access_token",value=f"Bearer {login_tokens.access_token}", httponly=True)
    response.set_cookie(key="refresh_token",value=f"Bearer {login_tokens.refresh_token}", httponly=True)
    return login_tokens

@router.put('/{user_id}/edit', tags=['users'], response_model=UserEditResponse)
async def update_user(request: Request, user_id:int, edit_user: UserEdit, service: UserService = Depends(get_user_service)):
    if user_id != request.state.user['id']:
        raise HTTPException(status_code=401, detail="유저 본인의 정보만 수정할 수 있습니다.")
    
    # jwt로 id검증 해야함
    edited_user = await service.edit_user(id=user_id,password=edit_user.password, username=edit_user.username, new_password=edit_user.new_password)
    return edited_user