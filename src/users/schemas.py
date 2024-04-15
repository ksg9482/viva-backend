from typing import Optional
from pydantic import BaseModel

class UserSignUp(BaseModel):
    username: str
    email: str
    password: str

class UserSignUpResponse(BaseModel):
    email: str

class UserLogin(BaseModel):
    email: str
    password: str 

class UserLoginResponse(BaseModel):
    email: str

class UserEdit(BaseModel):
    username: Optional[str]
    password: Optional[str]

class UserEditResponse(BaseModel):
    username: str
    email: str
    password: str