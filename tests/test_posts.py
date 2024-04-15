from fastapi import HTTPException
import pytest
from httpx import AsyncClient

# 게시글 작성
@pytest.mark.posts
async def test_create_post():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.post("/posts")
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert response.json() == {}

# 게시글 수정
@pytest.mark.posts
async def test_edit_post():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        post_id = 1
        response = await ac.put(f"/{post_id}/edit")
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert response.json() == {}

# 게시글 삭제
@pytest.mark.posts
async def test_delete_post():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        post_id = 1
        response = await ac.delete(f"/{post_id}")
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert response.json() == {}

# 게시글 목록
@pytest.mark.posts
async def test_get_posts():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.get("/")
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert response.json() == {}

# 게시글 조회
@pytest.mark.posts
async def test_get_post():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        post_id = 1
        response = await ac.get(f"/{post_id}")
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert response.json() == {}