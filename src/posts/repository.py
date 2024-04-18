from typing import Union
from fastapi import Depends, HTTPException
from posts.models import Post, PostView

from sqlalchemy import CursorResult, insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db


class PostRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def find_by_id(self, id: int) -> Union[Post, None]:
        try:
            # 조회수 올리기
            result:CursorResult = await self.db.execute(
                select(Post).where(Post.id == id)
                )
            post = result.scalars().first()
            return post
        except Exception as e:
            print(e)
            raise Exception(detail='Post find by id fail')

    async def save(self, post: Post):
        try:
            self.db.add(post)
            await self.db.commit()
            await self.db.refresh(post)
            return post
        except Exception as e:
            print(e)
            raise Exception(detail='Post save fail')
        
    async def update(self, user_id:int, post: Post):
        try:
            await self.db.execute(update(Post).where(Post.id == post.id, Post.user_id == user_id).values(title=post.title, content=post.content))
            await self.db.commit()
            await self.db.refresh(post)
            return post
        except Exception as e:
            print(e)
            raise Exception(detail='Post update fail')
        
    async def delete(self, user_id:int, post_id: int):
        try:
            await self.db.execute(delete(Post).where(Post.id == post_id, Post.user_id == user_id))
            await self.db.commit()
        except Exception as e:
            print(e)
            raise Exception(detail='Post delete fail')
        
    async def find_all(self):
        try:
            result = await self.db.execute(select(Post))
            posts = result.scalars().all()
            return posts
        except Exception as e:
            print(e)
            raise Exception(detail='Post find all fail')
    
def get_post_repo(repo: PostRepository=Depends(PostRepository)):
    return repo