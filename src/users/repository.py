from typing import Union
from fastapi import Depends, HTTPException, status
from src.users.models import User, RefreshToken

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base


class UserRepository:
    def __init__(self, db: AsyncSession = Depends(Base.get_db)):
        self.db = db

    async def find_by_id(self, id: int) -> Union[User, None]:
        result = await self.db.execute(select(User).where(User.id == id, User.deleted_at == None))
        user = result.scalars().first()
        return user
    
    async def find_by_email(self, email: str) -> Union[User, None]:
        result = await self.db.execute(select(User).where(User.email == email, User.deleted_at == None))
        user = result.scalars().first()
        return user

    async def save(self, user: User):
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='유저 저장에 실패했습니다.')
        
    async def edit_user(self, user: User):
        try:
            await self.db.execute(update(User).where(User.email == user.email).values(username=user.username, password=user.password))
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='유저 수정에 실패했습니다.')
        
    async def delete_soft_user(self, user: User):
        try:
            await self.db.execute(update(User).where(User.id == user.id).values(deleted_at=user.deleted_at))
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='유저 삭제에 실패했습니다.')
            
    async def save_refresh_token(self, user_id: int, refresh_token: str):
        try:
            result = await self.db.execute(select(RefreshToken).where(RefreshToken.user_id == user_id, User.deleted_at == None))
            finded_refresh_token = result.scalars().first()

            # refresh_token이 이미 존재하면 update
            if finded_refresh_token:
                if finded_refresh_token.token != refresh_token:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='유효한 refresh_token이 아닙니다.')
                
                await self.db.execute(update(RefreshToken).where(RefreshToken.user_id == user_id).values(refresh_token=refresh_token))
            # refresh_token이 없으면 insert
            else:
                new_refresh_token = RefreshToken(user_id=user_id, refresh_token=refresh_token)
                self.db.add(new_refresh_token)
            await self.db.commit()
            await self.db.refresh(RefreshToken)
            return RefreshToken
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='refresh_token 저장에 실패했습니다.')
        
def get_user_repo(repo: UserRepository=Depends(UserRepository)):
    return repo