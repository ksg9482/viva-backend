from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import timedelta, datetime
# jwt

JWT_SECRET_KEY = 'test'
JWT_ALGORITHM = 'HS256'

class UserUtills:
    def encode_access_token(self, id:int, email:str, username:str):
        if username :
            payload = {
                'exp': datetime.now() + timedelta(hours=1),
                'iat': datetime.now(),
                'scope': 'access_token', # 엑세스랑 리프레시 하려면 주입받는게?
                'data': {
                    'id': id,
                    'email': email,
                    'username': username
                }
            }
            return jwt.encode(
                payload,
                JWT_SECRET_KEY,
                algorithm=JWT_ALGORITHM
            )
        else :
            raise ValueError('username is None')
       
    # jwt class 만드는게 좋을지도?
    # def get_access_token(self, email:str, username:str) -> str:
    #     return self.encode_token(email, username)
    
    def encode_refresh_token(self, id:int, email:str, username:str):
        if username :
            payload = {
                'exp': datetime.now() + timedelta(hours=24),  # Refresh token의 유효기간을 7일로 설정
                'iat': datetime.now(),
                'scope': 'refresh_token',  # Scope를 refresh_token으로 설정
                'data': {
                    'id': id,
                    'email': email,
                    'username': username
                }
            }
            return jwt.encode(
                payload,
                JWT_SECRET_KEY,
                algorithm=JWT_ALGORITHM
            )
        else :
            raise ValueError('username is None')

    # def get_refresh_token(self, email:str, username:str) -> str:
    #     return self.encode_refresh_token(email, username)
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.exceptions.InvalidTokenError as e:
            e.args = ['Invalid token']
            return e