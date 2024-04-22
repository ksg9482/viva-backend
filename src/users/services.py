from datetime import timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from src.users.dependencies import get_hashed_password, verify_password
from src.users.models import User
from src.users.repository import UserRepository, get_user_repo
from src.auth.utills import JwtUtils, get_user_utills

class JWTTokens:
    def __init__(self, access_token:str, refresh_token:str):
        self.access_token = access_token
        self.refresh_token = refresh_token

class UserService:

    def __init__(
            self, 
            repo:UserRepository=Depends(get_user_repo), 
            utills:JwtUtils=Depends(get_user_utills)
        ):
        self.repo = repo
        self.utills = utills

    async def create_user_account(self, username: str, email: str, password: str) -> User:
        existing_user = await self.repo.find_by_email(email)
        if existing_user:
            raise HTTPException(status_code=400, detail='이미 가입된 사용자입니다.')

        hashed_password = get_hashed_password(password)
        new_user = User(username=username, email=email, password=hashed_password)
        try:
            await self.repo.save(new_user)
            return new_user
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail='회원가입이 실패했습니다. 기입한 내용을 확인해보세요')

    async def login(self, email: str, password: str):
        user = await self.repo.find_by_email(email)

        if user is None:
            raise HTTPException(status_code=400, detail='존재하지 않는 사용자입니다.')

        if self.valid_password(password, user.password) is False:
            raise HTTPException(status_code=401, detail="잘못된 비밀번호 입니다.")
        
        access_token = self.utills.encode_access_token(user.id, user.email, user.username, timedelta(hours=1))
        refresh_token = self.utills.encode_refresh_token(user.id, user.email, user.username, timedelta(hours=24))
        
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

    async def delete_user(self, user_id:int, password:str):
        user = await self.get_user(user_id)

        if self.valid_password(password, user.password) is False:
            raise HTTPException(status_code=401, detail="잘못된 비밀번호 입니다.")
        
        user.set_deleted_at()

        deleted_user = await self.repo.delete_soft_user(user)
        return deleted_user

    async def get_user(self, id:int) -> User:
        user = await self.repo.find_by_id(id)
        if user is None:
            raise HTTPException(status_code=400, detail='존재하지 않는 사용자입니다.')
        
        return user
    
    async def jwt_refresh(self, access_token:str, refresh_token:str):
        access_token_valid_options = {"verify_exp": False}
        if not self.utills.decode_token(access_token, access_token_valid_options) or not self.utills.decode_token(refresh_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다.",
            )
        user = self.utills.decode_token(refresh_token)
        user_id = user['data']['id']

        finded_user = await self.repo.find_by_id(user_id)
        if finded_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='존재하지 않는 사용자입니다.')

        access_token = self.utills.encode_access_token(finded_user.id, finded_user.email, finded_user.username, timedelta(hours=1))
        refresh_token = self.utills.encode_refresh_token(finded_user.id, finded_user.email, finded_user.username, timedelta(hours=24))
        await self.repo.save_refresh_token(refresh_token)

        return {'access_token': access_token, 'refresh_token': refresh_token}

    def valid_password(self, password, hasded_password) -> bool:
        return verify_password(password, hasded_password)
        

def get_user_service(service: UserService=Depends(UserService)):
    return service