from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(200))
    password = Column(String(512), min(8))
    created_at = Column(Date)
    updated_at = Column(Date)
    deleted_at = Column(Date)

    posts = relationship("Post", back_populates="posts")

    
