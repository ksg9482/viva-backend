from fastapi import Depends
from passlib.context import CryptContext
from users.repository import UserRepository
from users.utills import UserUtills

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_repo(repo: UserRepository=Depends(UserRepository)):
    return repo

def get_user_utills(utills: UserUtills=Depends(UserUtills)):
    return utills