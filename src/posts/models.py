from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from database import Base


class PostView(Base):
    __tablename__ = "post_view"
    id: int = Column(Integer, primary_key=True, index=True)
    view_count: int = Column(Integer, default=0)

    post = relationship("Post", back_populates="post_view")

    # 비즈니스 로직
    def increase_view_count(self):
        self.view_count += 1

class Post(Base):
    __tablename__ = "post"
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(100), nullable=False)
    content: str = Column(String(1000), nullable=False)
    created_at: DateTime = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at: DateTime = Column(DateTime, onupdate=func.now())

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts", lazy="joined")

    post_view_id: int = Column(Integer, ForeignKey('post_view.id'))
    post_view = relationship("PostView", back_populates="post", lazy="joined")

    # 비즈니스 로직
    def update_title(self, title: str):
        self.title = title

    def update_content(self, content: str):
        self.content = content