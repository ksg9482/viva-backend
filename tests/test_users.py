from fastapi import HTTPException
import pytest
from httpx import AsyncClient
from config import BASE_URL

# api 테스트

# 회원 가입
@pytest.mark.users
@pytest.mark.signup
async def test_signup_ok():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username":"test_user_name",
            "email":"test_email@test.com",
            "password":"test_Password_1!",
        }
        response = await ac.post("/users/signup", json=signup_user)
        status_code = response.status_code
        response_content = response.json()
        assert status_code == 201, "회원가입에 성공했을 때 상태코드 201을 반환해야 한다"
        assert response_content['password'] is None, "반환된 응답에는 비밀번호가 없어야 한다"
        assert response_content == {
            "username":"test_user_name",
            "email":"test_email@test.com"
        }, "회원가입에 성공했을 때 이름, 이메일을 반환해야 한다"
        # 유저는 이름, 이메일, 비밀번호를 포함해야 한다
        # 비밀번호 규칙은 8자 이상, 소문자, 대문자, 특수문자 각 1자리 이상 포함

@pytest.mark.users
@pytest.mark.signup
async def test_signup_password_length():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username":"test_user_name",
            "email":"test_email@test.com",
            "password":"aB!4567",
        }
        response = await ac.post("/users/signup", json=signup_user)
        status_code = response.status_code
        response_content = response.json()
        assert status_code == 422 # validation error
        assert response_content['detail'][0]['msg'] == 'String should have at least 8 characters', "비밀번호는 8자 미만이면 에러가 발생해야 한다."

@pytest.mark.users
@pytest.mark.signup
async def test_signup_password_lowercase():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username":"test_user_name",
            "email":"test_email@test.com",
            "password":"AB!45678",
        }
        response = await ac.post("/users/signup", json=signup_user)
        status_code = response.status_code
        response_content = response.json()
        assert status_code == 422
        assert response_content['detail'][0]['msg'] == 'Value error, Password must contain at least one lower character, one upper character, one special symbol', "비밀번호는 소문자를 하나 이상 포함하지 않으면 에러가 발생해야 한다."

@pytest.mark.users
@pytest.mark.signup
async def test_signup_password_uppercase():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username":"test_user_name",
            "email":"test_email@test.com",
            "password":"ab!45678",
        }
        response = await ac.post("/users/signup", json=signup_user)
        status_code = response.status_code
        response_content = response.json()
        assert status_code == 422
        assert response_content['detail'][0]['msg'] == 'Value error, Password must contain at least one lower character, one upper character, one special symbol', "비밀번호는 대문자를 하나 이상 포함하지 않으면 에러가 발생해야 한다."

@pytest.mark.users
@pytest.mark.signup
async def test_signup_password_special():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username":"test_user_name",
            "email":"test_email@test.com",
            "password":"abc45678",
        }
        response = await ac.post("/users/signup", json=signup_user)
        status_code = response.status_code
        response_content = response.json()
        assert status_code == 422
        assert response_content['detail'][0]['msg'] == 'Value error, Password must contain at least one lower character, one upper character, one special symbol', "비밀번호는 특수문자를 하나 이상 포함하지 않으면 에러가 발생해야 한다."

# 로그인
@pytest.mark.users
@pytest.mark.login
async def test_login_ok():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/users/login")
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert response.json() == {}

@pytest.mark.users
@pytest.mark.login
async def test_login_email():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/users/login")
        assert response.status_code == 500
        assert response.json() == {}, "이메일 형식에 맞는 이메일이어야 한다."

@pytest.mark.users
@pytest.mark.login
async def test_login_password():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/users/login")
        assert response.status_code == 500
        assert response.json() == {}, "정확한 비밀번호를 입력해야 한다."

# 회원정보 수정
@pytest.mark.users
@pytest.mark.user_edit
async def test_user_edit():
    async with AsyncClient(base_url=BASE_URL) as ac:
        user_id = 1
        response = await ac.put(f"/users/{user_id}/edit")
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert response.json() == {}

@pytest.mark.users
@pytest.mark.user_edit
async def test_user_edit_id():
    async with AsyncClient(base_url=BASE_URL) as ac:
        user_id = 1
        response = await ac.put(f"/users/{user_id}/edit")
        assert response.status_code == 500
        assert response.json() == {}, "가입한 아이디로 수정해야 한다."

@pytest.mark.users
@pytest.mark.user_edit
async def test_user_edit_password():
    async with AsyncClient(base_url=BASE_URL) as ac:
        user_id = 1
        response = await ac.put(f"/users/{user_id}/edit")
        assert response.status_code == 500
        assert response.json() == {}, "변경할 비밀번호가 8자 이상이어야 한다."

# 이하 비밀번호 로직