from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from database import Base

# 일정시간동안 업데이트 쿼리 모아서 처리하는 등 빈번한 view_count 해소 필요
# https://supreme-ys.tistory.com/186
class PostView(Base):
    __tablename__ = "post_view"
    id: int = Column(Integer, primary_key=True, index=True)
    post_id: int = Column(Integer, ForeignKey('post.id'))
    view_count: int = Column(Integer, default=0)

    post = relationship("Post", back_populates="post_view")

    # 비즈니스 로직
    def increase_view_count(self):
        # 객체가 아니라 db저장된 거 처리하는게 더 좋을지도?
        self.view_count += 1

class Post(Base):
    __tablename__ = "post"
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(100), unique=True, index=True)
    content: str = Column(String(1000))
    created_at: DateTime = Column(DateTime, server_default=func.now(),  nullable=False)
    updated_at: DateTime = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")

    post_view = relationship("PostView", back_populates="post")

    # 비즈니스 로직
    def update_title(self, title: str):
        self.title = title

    def update_content(self, content: str):
        self.content = content

    # def increase_view_count_process(self):
    #     self.post_view.increase_view_count()