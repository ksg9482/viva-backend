from enum import Enum
from typing import Union
from fastapi import Depends, HTTPException, logger
from posts.models import Post, PostView

from sqlalchemy import CursorResult, insert, select, update, delete
from sqlalchemy.orm import aliased, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db


class PostSortEnum(Enum):
    VIEW_COUNT = 'view_count'
    CREATED_AT = 'created_at'

class PostRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    # async def find_by_id(self, id: int) -> Union[Post, None]:
    #     try:
    #         # 조회수 올리기
    #         result:CursorResult = await self.db.execute(
    #             select(Post).where(Post.id == id)
    #         )
    #         post = result.scalars().first()
    #         return post
    #     except Exception as e:
    #         print(e)
    #         raise Exception(detail='Post find by id fail')
        
    async def get_post_detail(self, post_id: int) -> Union[Post, None]:
        print('repository get_post_detail')
        try:
            result:CursorResult = await self.db.execute(
                select(Post)
                .where(Post.id == post_id)
            )
            post = result.scalars().first()
            if post:
                post.post_view.increase_view_count()
                await self.db.execute(update(PostView).where(PostView.id == post.post_view_id).values(view_count=post.post_view.view_count))
                await self.db.commit()
                await self.db.refresh(post)
            return post
        except Exception as e:
            print(e)
            raise Exception(detail='Post find by id fail')
        
    async def save(self, post: Post):
        logger.logger.debug('post repository save')
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
        
    async def find_all(self, page: int = 1, items_per_page: int = 20, sort_option: PostSortEnum = PostSortEnum.CREATED_AT):
        def sort_option_converter(sort_option:PostSortEnum):
            if sort_option == PostSortEnum.VIEW_COUNT:
                return PostView.view_count.desc()
            else:
                return Post.created_at.desc()

        offset = (page - 1) * items_per_page

        try:
            result = await self.db.execute(
                select(Post)
                .join(Post.post_view)
                .order_by(sort_option_converter(sort_option))
                .limit(items_per_page)
                .offset(offset)
            )
            posts = result.scalars()._allrows()
            return posts
        except Exception as e:
            print(e)
            raise Exception('Post find all fail')
    
def get_post_repo(repo: PostRepository=Depends(PostRepository)):
    return repo