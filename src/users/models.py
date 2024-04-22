from typing import Optional
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="refresh_token", lazy='joined')

class User(Base):
    __tablename__ = "users" #db에 이미 user 테이블이 있음. 그래서 users로 변경
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(200), index=True)
    password: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, onupdate=func.now(), nullable=True)
    deleted_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    posts = relationship("Post", back_populates="user")
    UniqueConstraint('username', 'deleted_at', name='unique_username')

    refresh_token = relationship("RefreshToken", back_populates="user")

    # 비즈니스 로직
    def update_username(self, username: str):
        self.username = username

    def update_password(self, password: str):
        self.password = password

    def set_deleted_at(self, date:Optional[DateTime] = func.now()):
        self.deleted_at = date
    
