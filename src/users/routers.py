from fastapi import APIRouter, Depends, HTTPException, logger

from users.schemas import UserSignUp, UserSignUpResponse
from users.services import create_user_account

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

router = APIRouter(prefix='/users', tags=['users'])

@router.post('/signup', response_model=UserSignUpResponse,tags=['users'])
async def signup(signup_user: UserSignUp, db: AsyncSession = Depends(get_db)):
    try:
        created_user = await create_user_account(username=signup_user.username, email=signup_user.email, password=signup_user.password, db=db)
        return created_user
    except Exception as e:
        # logger
        print(e)
        raise HTTPException(status_code=500)

@router.post('/login', tags=['users'])
async def login():
    raise HTTPException(status_code=500)

@router.put('/{user_id}/edit', tags=['users'])
async def update_user():
    raise HTTPException(status_code=500)