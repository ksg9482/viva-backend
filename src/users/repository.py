from typing import Union
from fastapi import Depends, HTTPException
from users.models import User

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db


class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def find_by_id(self, id: int) -> Union[User, None]:
        result = await self.db.execute(select(User).where(User.id == id))
        user = result.scalars().first()
        return user
    
    async def find_by_email(self, email: str) -> Union[User, None]:
        result = await self.db.execute(select(User).where(User.email == email))
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
            raise Exception(detail='User data save fail')
        
    async def edit_user(self, user: User):
        try:
            await self.db.execute(update(User).where(User.email == user.email).values(username=user.username, password=user.password))
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            print(e)
            raise Exception(detail='User data edit fail')
    
def get_user_repo(repo: UserRepository=Depends(UserRepository)):
    return repo