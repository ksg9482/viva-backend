from typing import Optional
from fastapi import Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from users.dependencies import get_hashed_password, verify_password
from users.models import User
from users.repository import UserRepository, get_user_repo
from users.utills import UserUtills, get_user_utills

class JWTTokens:
    def __init__(self, access_token:str, refresh_token:str):
        self.access_token = access_token
        self.refresh_token = refresh_token

class UserService:

    def __init__(
            self, 
            repo:UserRepository=Depends(get_user_repo), 
            db:AsyncSession=Depends(get_db), 
            utills:UserUtills=Depends(get_user_utills)
        ):
        self.repo = repo
        self.db = db
        self.utills = utills

    async def create_user_account(self, username: str, email: str, password: str) -> User:
        await self.valid_duplicate_user(email)

        hashed_password = get_hashed_password(password)
        new_user = User(username=username, email=email, password=hashed_password)
        try:
            result = await self.repo.save(new_user)
            return result
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail='회원가입이 실패했습니다. 기입한 내용을 확인해보세요')

    async def login(self, email: str, password: str):
        # 이메일로 찾는건 여기서만??
        user = await self.repo.find_by_email(email)

        if user is None:
            raise HTTPException(status_code=400, detail='존재하지 않는 사용자입니다.')

        if self.valid_password(password, user.password) is False:
            raise HTTPException(status_code=401, detail="잘못된 비밀번호 입니다.")
        
        access_token = self.utills.encode_access_token(user.id, user.email, user.username)
        refresh_token = self.utills.encode_refresh_token(user.id, user.email, user.username)
        
        tokens = JWTTokens(access_token, refresh_token)
        return tokens

    async def edit_user(self, id:int, password:str, username:Optional[str]=None, new_password:Optional[str]=None) -> User:
        user = await self.get_user(id)
        if self.valid_password(password, user.password) is False:
            raise HTTPException(status_code=401, detail="잘못된 비밀번호 입니다.")
        
        if username:
            user.update_username(username)

        if new_password:
            user.update_password(get_hashed_password(new_password))

        try:
            result = await self.repo.edit_user(user)
            return result
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail='회원정보 수정이 실패했습니다. 기입한 내용을 확인해보세요')

        """
        - 회원 본인만 수정가능합니다.
- 수정시에는 기존 비밀번호를 입력받고 유효성 검증을 해주세요
- 사용자 이름 및 비밀번호를 수정가능합니다.
        """
    async def get_user(self, id:int) -> User:
        user = await self.repo.find_by_id(id)
        if user is None:
            raise HTTPException(status_code=400, detail='존재하지 않는 사용자입니다.')
        
        return user
    
    # 로직통일, 에러 관리등 일원화
    async def valid_duplicate_user(self, email):
        existing_user = await self.repo.find_by_email(email)
        if existing_user:
            raise HTTPException(status_code=400, detail='이미 가입된 사용자입니다.')

    def valid_password(self, password, hasded_password) -> bool:
            return verify_password(password, hasded_password)
        

def get_user_service(service: UserService=Depends(UserService)):
    return service