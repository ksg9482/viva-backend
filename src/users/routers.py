from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/users')

@router.post('/sigup')
async def signup():
    raise HTTPException(status_code=500)

@router.post('/login')
async def login():
    raise HTTPException(status_code=500)

@router.put('/user')
async def update_user():
    raise HTTPException(status_code=500)