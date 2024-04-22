from enum import Enum
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.users.models import User

class PostView(Base):
    __tablename__ = "post_view"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)

    post = relationship("Post", back_populates="post_view")

    # 비즈니스 로직
    def increase_view_count(self):
        self.view_count += 1

class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(10000), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped[User] = relationship("User", back_populates="posts", lazy="joined")

    post_view_id: Mapped[int] = mapped_column(Integer, ForeignKey('post_view.id'))
    post_view = relationship("PostView", back_populates="post", lazy="joined", cascade="all")

    # 비즈니스 로직
    def update_title(self, title: str):
        self.title = title

    def update_content(self, content: str):
        self.content = content

    def add_username(self, username: str):
        self.username = username

    def add_view_count(self, view_count: int):
        self.view_count = view_count

class PostSortEnum(Enum):
    VIEW_COUNT = 'view_count'
    CREATED_AT = 'created_at'