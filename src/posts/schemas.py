from datetime import date
from typing import Optional
from pydantic import BaseModel

class CreatePost(BaseModel):
    title: str
    content: str

class CreatePostResponse(BaseModel):
    title: str
    content: str
    created_at: date
    update_at: date

class EditPost(BaseModel):
    title: str
    content: str

class EditPostResponse(BaseModel):
    title: str
    content: str
    created_at: date
    update_at: date

class Post(BaseModel):
    title: str
    author: str
    view_count: int

class PostsReponse(BaseModel):
    Posts: list[Post]

class PostDetailReponse(BaseModel):
    title: str
    author: str
    content: str
    created_at: date
    update_at: date