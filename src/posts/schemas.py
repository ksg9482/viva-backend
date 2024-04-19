from datetime import date, datetime
from typing import List, Optional, Union
from pydantic import BaseModel, field_serializer

class CreatePost(BaseModel):
    title: str
    content: str

class CreatePostResponse(BaseModel):
    id:int
    title: str
    content: str

class EditPost(BaseModel):
    title: str
    content: str

class EditPostResponse(BaseModel):
    id:int
    title: str
    content: str

class Post(BaseModel):
    id:int
    title: str
    username: str
    view_count: int

class PostsReponse(BaseModel):
    posts: list[Post]

class PostDetailReponse(BaseModel):
    id:int
    title: str
    username: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime]

    @field_serializer('updated_at', when_used='json')
    def serialize_updated_at_empty_str(updated_at: Optional[datetime]):
        if updated_at == None:
            return ""
        
        return updated_at
