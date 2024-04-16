from sqlalchemy import Column, DateTime, Integer, String, Date, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from database import Base

class User(Base):
    __tablename__ = "users" #db에 이미 user 테이블이 있음. 그래서 users로 변경
    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String(100), unique=True, index=True)
    email: str = Column(String(200))
    password: str = Column(String(512))
    created_at: DateTime = Column(DateTime, server_default=func.now(),  nullable=False)
    updated_at: DateTime = Column(DateTime, onupdate=func.now())
    deleted_at: DateTime = Column(DateTime)

    posts = relationship("Post", back_populates="user")
    UniqueConstraint('username', 'deleted_at', name='unique_username')

    # 비즈니스 로직
    def update_username(self, username: str):
        self.username = username

    def update_password(self, password: str):
        self.password = password
    
