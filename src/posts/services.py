from typing import List, Optional
from fastapi import Depends, HTTPException

from src.posts.models import Post, PostView, PostSortEnum
from src.posts.repository import PostRepository, get_post_repo


class PostService:
    def __init__(
            self, 
            repo:PostRepository=Depends(get_post_repo), 
        ):
        self.repo = repo

    async def create_post(self, user_id:int, title:str, content:str):
        new_post_view = PostView()
        new_post = Post(user_id=user_id, title=title, content=content, post_view=new_post_view)

        return await self.repo.save(new_post)

    async def update_post(self, user_id:int, post_id: int, title:str, content:str):
        post = await self.repo.find_post_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=400, detail='존재하지 않는 포스트입니다.')
        
        if post.user_id != user_id:
            raise HTTPException(status_code=401, detail='작성자 본인만 수정가능 합니다.')

        if title:
            post.update_title(title)

        if content:
            post.update_content(content)

        return await self.repo.update(user_id, post)
        

    async def delete_post(self, user_id:int, post_id: int):
        post = await self.repo.find_post_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=400, detail='존재하지 않는 포스트입니다.')
        
        if post.user_id != user_id:
            raise HTTPException(status_code=401, detail='작성자 본인만 삭제가능 합니다.')
        
        await self.repo.delete(user_id, post_id)
        return post

    async def get_posts(
            self, 
            page: int = 1, 
            items_per_page: int = 20, 
            sort_option: Optional[PostSortEnum] = PostSortEnum.CREATED_AT
        ):
        finded_posts = await self.repo.find_all(page, items_per_page, sort_option)

        posts = self._post_form_changer(finded_posts)
        return posts

    def _post_form_changer(self, finded_posts:List[Post]):
        for post in finded_posts:
            username = self._username_selector(post)
            post.add_username(username)
            post.add_view_count(post.post_view.view_count)
        return finded_posts
    
    def _username_selector(self, post:Post):
        deleted_username = '탈퇴한 유저'
        return post.user.username if post.user.deleted_at is None else deleted_username
    
    async def get_post(self, post_id: int) -> Post:
        post = await self.repo.get_post_detail(post_id)
        if post is None:
            raise HTTPException(status_code=400, detail='존재하지 않는 포스트입니다.')
        
        post.add_username(post.user.username)
        return post

def get_post_service(service: PostService = Depends(PostService)):
    return service