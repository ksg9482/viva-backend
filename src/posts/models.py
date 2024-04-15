from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from database import Base

class Post(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, index=True)
    content = Column(String)
    created_at = Column(Date)
    updated_at = Column(Date)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")