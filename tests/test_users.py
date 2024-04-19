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
            "username":"test_user_name_signup_ok",
            "email":"test_email_signup_ok@test.com",
            "password":"test_Password_1!",
        }
        response = await ac.post("/users/signup", json=signup_user)
        status_code = response.status_code
        response_content = response.json()
        assert response_content.get('password') is None, "반환된 응답에는 비밀번호가 없어야 한다"
        assert response_content == {
            "username":"test_user_name_signup_ok",
            "email":"test_email_signup_ok@test.com"
        }, "회원가입에 성공했을 때 이름, 이메일을 반환해야 한다"
        assert status_code == 201, "회원가입에 성공했을 때 상태코드 201을 반환해야 한다"


@pytest.mark.users
@pytest.mark.signup
async def test_signup_duplicate():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username":"test_user_name_signup_ok",
            "email":"test_email_signup_ok@test.com",
            "password":"test_Password_1!",
        }
        response = await ac.post("/users/signup", json=signup_user)
        status_code = response.status_code
        response_content = response.json()
        assert status_code == 400, "중복 가입일 경우 상태코드 400을 반환해야 한다"
        print(response_content)
        assert response_content.get('detail') == '이미 가입된 사용자입니다.', "중복 가입일 경우 이미 가입된 사용자임을 밝히는 예외가 발생해야 한다."


@pytest.mark.users
@pytest.mark.signup
async def test_signup_password_length():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username":"test_user_name_signup_password",
            "email":"test_email_signup_password@test.com",
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
            "username":"test_user_name_signup_lowercase",
            "email":"test_email_signup_lowercase@test.com",
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
            "username":"test_user_name_signup_upppercase",
            "email":"test_email_signup_upppercase@test.com",
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
            "username":"test_user_name_special",
            "email":"test_email_special@test.com",
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
        signup_user = {
            "username":"test_user_name",
            "email":"test_email@test.com",
            "password":"test_Password_1!",
        }
        await ac.post("/users/signup", json=signup_user)

        login_user = {
            "email": "test_email@test.com", 
            "password": "test_Password_1!"
        }

        response = await ac.post("/users/login", json=login_user)
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert isinstance(response.json()['access_token'], str), "access_token은 문자열이어야 한다."
        assert isinstance(response.json()['refresh_token'], str), "refresh_token은 문자열이어야 한다."

        # 유효하지 않은 사용자 로그인
        

@pytest.mark.users
@pytest.mark.login
async def test_login_email():
    async with AsyncClient(base_url=BASE_URL) as ac:
        login_user = {
            "email": "invalid_password", 
            "password": "test_Password_1!"
        }
        # with pytest.raises(HTTPException):
        response = await ac.post("/users/login", json=login_user)
        assert response.status_code == 422, "이메일 형식에 맞지 않은 이메일을 입력하면 상태코드 422를 반환해야 한다."
        assert response.json()['detail'][0]['msg'] == 'value is not a valid email address: The email address is not valid. It must have exactly one @-sign.',"이메일 형식에 맞지 않은 이메일을 입력하면 예외가 발생해야 한다."

@pytest.mark.users
@pytest.mark.login
async def test_login_password():
    async with AsyncClient(base_url=BASE_URL) as ac:
        login_user = {
            "email": "test_email@test.com", 
            "password": "invalid_password"
        }
        # with pytest.raises(HTTPException):
        response = await ac.post("/users/login", json=login_user)
        assert response.status_code == 401, "유효하지 않은 사용자 로그인 정보를 제공하면 상태 코드 401을 반환해야 한다."
        assert response.json()['detail'] == '잘못된 비밀번호 입니다.', "잘못된 비밀번호를 입력하면 예외가 발생해야 한다."


# 회원정보 수정
@pytest.mark.users
@pytest.mark.user_edit
async def test_user_edit_ok():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username":"test_user_name_edit_ok",
            "email":"test_email_edit_ok@test.com",
            "password":"test_Password_1!",
        }
        await ac.post("/users/signup", json=signup_user)
        login_response =await ac.post("/users/login", json={"email": signup_user["email"], "password": signup_user["password"]})
        login_response_content = login_response.json()
        access_token = login_response_content['access_token']
        cookies = {"access_token": access_token}
        user_id = login_response_content.get('id')

        user_edit_content = {
            "password":"test_Password_1!",
            "username":"test_user_name_edit_ok",
            "new_password":"test_Password_2!"
        }
        response = await ac.put(f"/users/edit", json=user_edit_content, cookies=cookies)
        
        assert response.json() == {
            "email":"test_email_edit_ok@test.com", # id가 좋을까??
            "username":"test_user_name_edit_ok",
        }, "수정된 정보를 반환해야 한다."
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"


# @pytest.mark.users
# @pytest.mark.user_edit
# async def test_user_edit_id():
#     async with AsyncClient(base_url=BASE_URL) as ac:
#         signup_user = {
#             "username":"test_user_name",
#             "email":"test_email@test.com",
#             "password":"test_Password_1!",
#         }
#         await ac.post("/users/signup", json=signup_user)
#         login_response =await ac.post("/users/login", json={"email": signup_user["email"], "password": signup_user["password"]})
#         login_response_content = login_response.json()
#         access_token = login_response_content['access_token']
#         cookies = {"access_token": access_token}
#         user_id = 9999

#         user_edit_content = {
#             "password":"test_Password_1!",
#             "username":"test_user_name",
#             "new_password":"test_Password_2!"
#         }

#         response = await ac.put(f"/users/edit", json=user_edit_content, cookies=cookies)
#         assert response.json()['detail'] == '유저 본인의 정보만 수정할 수 있습니다.', "가입한 아이디로 수정해야 한다."
#         assert response.status_code == 401, "상태코드 401을 반환해야 한다"


@pytest.mark.users
@pytest.mark.user_edit
async def test_user_edit_short_password():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username":"test_user_name_edit_password",
            "email":"test_email_edit_password@test.com",
            "password":"test_Password_1!",
        }
        await ac.post("/users/signup", json=signup_user)
        login_response =await ac.post("/users/login", json={"email": signup_user["email"], "password": signup_user["password"]})
        login_response_content = login_response.json()
        print(login_response_content)
        access_token = login_response_content['access_token']
        cookies = {"access_token": access_token}
        user_id = login_response_content.get('id')

        user_edit_content = {
            "password":"test_Password_1!",
            "username":"test_user_name_edit_password",
            "new_password":"1234567"
        }
        response = await ac.put(f"/users/edit", json=user_edit_content, cookies=cookies)
        response_content = response.json()

        assert response_content['detail'][0]['msg'] == 'String should have at least 8 characters', "비밀번호는 8자 미만이면 에러가 발생해야 한다."
        # assert response_content['detail'][0]['msg'] == 'Value error, Password must contain at least one lower character, one upper character, one special symbol', "변경할 비밀번호가 8자 이상, 대문자 1개 이상, 소문자 1개 이상, 특수문자 1개 이상을 준수하지 않으면 에러가 발생한다."
        assert response.status_code == 422, "상태코드 422을 반환해야 한다"

# 이하 비밀번호 로직