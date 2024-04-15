from fastapi import HTTPException
import pytest
from httpx import AsyncClient

# 회원 가입
@pytest.mark.users
async def test_signup():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        signup_user = {
            "username":"test_user_name",
            "email":"test_email@test.com",
            "password":"test_Password_1!",
        }
        response = await ac.post("/users/signup", json=signup_user)
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert response.json() == {}
        # 유저는 이름, 이메일, 비밀번호를 포함해야 한다
        # 단방향 암호화를 적용
        # 비밀번호 규칙은 8자 이상, 소문자, 대문자, 특수문자 각 1자리 이상 포함

# 로그인
@pytest.mark.users
async def test_login():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.post("/users/login")
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert response.json() == {}

# 회원정보 수정
@pytest.mark.users
async def test_user_edit():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        user_id = 1
        response = await ac.put(f"/users/{user_id}/edit")
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert response.json() == {}
