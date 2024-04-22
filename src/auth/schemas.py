import re
from pydantic import BaseModel, Field, field_validator, EmailStr

PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).+$" # [a-z] 소문자 검증, [A-Z] 대문자 검증, [\W] 특수문자 검증

class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(
        min_length=8, 
        description="비밀번호는 8자 이상, 소문자, 대문자, 특수문자 각 1자리 이상 포함",
    )

    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not re.match(PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "one special symbol"
            )
        return password

class UserSignUpResponse(BaseModel):
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str 

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str

class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str