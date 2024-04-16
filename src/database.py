from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True) # echo -> 내부에서 어떻게 동작하는지 확인용. 디버깅

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False, 
    bind=engine,
    class_=AsyncSession
    )

Base = declarative_base()