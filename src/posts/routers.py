from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/posts')

@router.post('/')
async def create_post():
    raise HTTPException(status_code=500)

@router.put('/{post_id}/edit')
async def update_post(post_id):
    raise HTTPException(status_code=500)

@router.delete('/{post_id}')
async def delete_post(post_id):
    raise HTTPException(status_code=500)

@router.get('/')
async def get_posts():
    raise HTTPException(status_code=500)

@router.get('/{post_id}')
async def get_post(post_id):
    raise HTTPException(status_code=500)