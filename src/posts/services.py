from typing import Optional
from fastapi import Depends, HTTPException, logger
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

from posts.models import Post, PostView
from posts.repository import PostRepository, get_post_repo


class PostService:
    def __init__(
            self, 
            repo:PostRepository=Depends(get_post_repo), 
            db:AsyncSession=Depends(get_db), 
        ):
        self.repo = repo
        self.db = db

    async def create_post(self, user_id:int, title:str, content:str):
        logger.logger.debug('create_post service')
        new_post_view = PostView()
        new_post = Post(user_id=user_id, title=title, content=content, post_view=new_post_view)
        created_post = await self.repo.save(new_post)
        return created_post

    async def update_post(self, user_id:int, post_id: int, title:str, content:str):
        post = await self.get_post(post_id)

        if title:
            post.update_title(title)

        if content:
            post.update_content(content)

        try:
            result = await self.repo.update(user_id, post)
            return result
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail='회원정보 수정이 실패했습니다. 기입한 내용을 확인해보세요')

    async def delete_post(self, user_id:int, post_id: int):
        post = await self.get_post(post_id)
        if post.user_id != user_id:
            raise HTTPException(status_code=401, detail='작성자 본인만 삭제가능 합니다.')
        
        await self.repo.delete(user_id, post_id)
        return post.id

    async def get_posts(self):
        posts = await self.repo.find_all()
        return posts

    async def get_post(self, post_id: int) -> Post:
        post = await self.repo.find_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=400, detail='존재하지 않는 포스트입니다.')
        
        return post

def get_post_service(service: PostService = Depends(PostService)):
    return service