from typing import Union
from fastapi import Depends, HTTPException, status
from src.posts.models import Post, PostSortEnum, PostView

from sqlalchemy import CursorResult, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base


class PostRepository:
    def __init__(self, db: AsyncSession = Depends(Base.get_db)):
        self.db = db
    async def find_post_by_id(self, post_id: int) -> Union[Post, None]:
        try:
            result = await self.db.execute(
                select(Post)
                .where(Post.id == post_id)
            )
            post = result.scalars().first()
            return post
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='게시글 찾기에 실패했습니다.')
    
    async def get_post_detail(self, post_id: int) -> Union[Post, None]:
        try:
            result:CursorResult = await self.db.execute(
                select(Post)
                .where(Post.id == post_id)
            )
            post = result.scalars().first()
            if post is None:
                return None
            
            post.post_view.increase_view_count()
            await self.db.execute(update(PostView).where(PostView.id == post.post_view_id).values(view_count=post.post_view.view_count))
            await self.db.commit()
            await self.db.refresh(post)
            return post
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='게시글 찾기에 실패했습니다.')
        
    async def save(self, post: Post):
        try:
            self.db.add(post)
            await self.db.commit()
            await self.db.refresh(post)
            return post
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail='게시글 저장에 실패했습니다.')
        
    async def update(self, user_id:int, post: Post):
        try:
            await self.db.execute(update(Post).where(Post.id == post.id, Post.user_id == user_id).values(title=post.title, content=post.content))
            await self.db.commit()
            await self.db.refresh(post)
            return post
        except Exception as e:
            raise HTTPException(status_code=500, detail='게시글 수정에 실패했습니다.')
        
    async def delete(self, user_id:int, post_id: int):
        try:
            await self.db.execute(delete(Post).where(Post.id == post_id, Post.user_id == user_id))
            await self.db.commit()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail='게시글 삭제에 실패했습니다.')
        
    async def find_all(self, page: int = 1, items_per_page: int = 20, sort_option: PostSortEnum = PostSortEnum.CREATED_AT):
        offset = (page - 1) * items_per_page

        try:
            result = await self.db.execute(
                select(Post)
                .join(Post.post_view)
                .order_by(self._sort_option_converter(sort_option))
                .limit(items_per_page)
                .offset(offset)
            )
            posts = result.scalars()._allrows()
            return posts
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='게시글 찾기에 실패했습니다.')
        
    def _sort_option_converter(self, sort_option:PostSortEnum):
            if sort_option == PostSortEnum.VIEW_COUNT:
                return PostView.view_count.desc()
            else:
                return Post.created_at.desc()
        
def get_post_repo(repo: PostRepository=Depends(PostRepository)):
    return repo