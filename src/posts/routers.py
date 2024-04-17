from fastapi import APIRouter, Depends, HTTPException

from posts.schemas import CreatePost, CreatePostResponse, EditPost, EditPostResponse, PostDetailReponse, PostsReponse
from posts.services import PostService, get_post_service

router = APIRouter(prefix='/posts', tags=['posts'])

@router.post('/', response_model=CreatePostResponse, tags=['posts'])
async def create_post(post:CreatePost, service: PostService = Depends(get_post_service)):
    user_id = 1
    created_post = await service.create_post(user_id, post.title, post.content)
    return created_post

@router.put('/{post_id}/edit', response_model=EditPostResponse, tags=['posts'])
async def update_post(post_id:int, edit_post:EditPost, service:PostService = Depends(get_post_service)):
    user_id = 1
    updated_post = await service.update_post(user_id, post_id, edit_post.title, edit_post.content)
    return updated_post

@router.delete('/{post_id}', tags=['posts'])
async def delete_post(post_id:int, service: PostService = Depends(get_post_service)):
    user_id = 1
    deleted_Post_id = await service.delete_post(user_id, post_id)
    return deleted_Post_id

@router.get('/', response_model=PostsReponse,tags=['posts'])
async def get_posts(service: PostService = Depends(get_post_service)):
    posts = await service.get_posts()
    return posts

@router.get('/{post_id}', response_model=PostDetailReponse, tags=['posts'])
async def get_post(post_id:int, service: PostService = Depends(get_post_service)):
    post = await service.get_post(post_id)
    return post