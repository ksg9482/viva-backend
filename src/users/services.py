from fastapi import Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from users.dependencies import get_hashed_password
from users.models import User


async def create_user_account(username: str, email: str, password: str, db: AsyncSession = Depends(get_db)) -> User:
    print(db)
    result = await db.execute(select(User).where(User.username == username))
    print(result)

    existing_user = result.scalars().first()
    print(existing_user)

    if existing_user:
        raise HTTPException(status_code=400, detail='이미 가입된 사용자명입니다.')
    
    hashed_password = get_hashed_password(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.add(new_user)

    try:
        await db.commit()
    except Exception as e:
        print('signup commit error')
        print(e)
        raise HTTPException(status_code=500, detail='회원가입이 실패했습니다. 기입한 내용을 확인해보세요')
    await db.refresh(new_user)

    return new_user