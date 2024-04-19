from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, logger, status

from posts.repository import PostSortEnum
from posts.schemas import CreatePost, CreatePostResponse, EditPost, EditPostResponse, PostDetailReponse, PostsReponse
from posts.services import PostService, get_post_service

router = APIRouter(prefix='/posts', tags=['posts'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CreatePostResponse, tags=['posts'])
async def create_post(request: Request, post:CreatePost, service: PostService = Depends(get_post_service)):
    logger.logger.debug('create_post router')
    user_id = request.state.user['id']
    created_post = await service.create_post(user_id, post.title, post.content)
    
    return created_post

@router.put('/{post_id}/edit', status_code=status.HTTP_200_OK, response_model=EditPostResponse, tags=['posts'])
async def update_post(request: Request, post_id:int, edit_post:EditPost, service:PostService = Depends(get_post_service)):
    user_id = request.state.user['id']
    updated_post = await service.update_post(user_id, post_id, edit_post.title, edit_post.content)
    return updated_post

@router.delete('/{post_id}', status_code=status.HTTP_200_OK, tags=['posts'])
async def delete_post(request: Request, post_id:int, service: PostService = Depends(get_post_service)):
    user_id = request.state.user['id']
    deleted_Post_id = await service.delete_post(user_id, post_id)
    return {"deleted_id": deleted_Post_id}

@router.get('/', status_code=status.HTTP_200_OK, response_model=PostsReponse,tags=['posts'])
async def get_posts(
    sort_option: Optional[PostSortEnum] = Query(None), 
    page: Optional[int] = Query(1),
    service: PostService = Depends(get_post_service)
    ):
    default_limit = 20
    posts = await service.get_posts(page, default_limit, sort_option)
    return {"posts": posts}

@router.get('/{post_id}', status_code=status.HTTP_200_OK, response_model=PostDetailReponse, tags=['posts'])
async def get_post(post_id:int, service: PostService = Depends(get_post_service)):
    post = await service.get_post(post_id)
    return post