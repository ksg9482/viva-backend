from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

class CreatePost(BaseModel):
    title: str
    content: str

class CreatePostResponse(BaseModel):
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

class EditPost(BaseModel):
    title: str
    content: str

class EditPostResponse(BaseModel):
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

class Post(BaseModel):
    title: str
    author: str
    view_count: int

class PostsReponse(BaseModel):
    posts: list[Post]

class PostDetailReponse(BaseModel):
    title: str
    username: str
    content: str
    created_at: datetime
    updated_at: datetime