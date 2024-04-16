from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/posts', tags=['posts'])

@router.post('/', tags=['posts'])
async def create_post():
    raise HTTPException(status_code=500)

@router.put('/{post_id}/edit', tags=['posts'])
async def update_post(post_id):
    raise HTTPException(status_code=500)

@router.delete('/{post_id}', tags=['posts'])
async def delete_post(post_id):
    raise HTTPException(status_code=500)

@router.get('/', tags=['posts'])
async def get_posts():
    raise HTTPException(status_code=500)

@router.get('/{post_id}', tags=['posts'])
async def get_post(post_id):
    raise HTTPException(status_code=500)