from fastapi import HTTPException
import pytest
import httpx
import asyncio
from httpx import AsyncClient
from config import BASE_URL

@pytest.fixture(scope="module") # 이거 결국 로그인으로 해야 토큰 얻을듯?
async def signup_user():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username": "test_user_name",
            "email": "test_email@test.com",
            "password": "test_Password_1!",
        }
        await ac.post("/users/signup", json=signup_user)
        login_response = await ac.post("/users/login", json={"email": signup_user["email"], "password": signup_user["password"]})
        login_response_content = login_response.json()
        access_token = login_response_content['access_token']
        signup_user['access_token'] = access_token
        return signup_user

    
# 게시글 작성
@pytest.mark.posts
async def test_create_post():

    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username": "test_user_name",
            "email": "test_email@test.com",
            "password": "test_Password_1!",
        }
        await ac.post("/users/signup", json=signup_user)
        login_response = await ac.post("/users/login", json={"email": signup_user["email"], "password": signup_user["password"]})
        login_response_content = login_response.json()
        access_token = login_response_content['access_token']

        cookies = {"access_token": access_token}
        create_post_data = {
            "title":"test_title",
            "content":"test_content",
        }
        response = await ac.post("/posts/", json=create_post_data, cookies=cookies)
        response_content = response.json()
        assert response.status_code == 201, "상태코드 201을 반환해야 한다"
        assert response_content['title'] == "test_title", "제목이 일치해야 한다"
        assert response_content['content'] == "test_content", "내용이 일치해야 한다"

# 게시글 수정
@pytest.mark.posts
async def test_edit_post():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username": "test_user_name",
            "email": "test_email@test.com",
            "password": "test_Password_1!",
        }
        await ac.post("/users/signup", json=signup_user)
        login_response = await ac.post("/users/login", json={"email": signup_user["email"], "password": signup_user["password"]})
        login_response_content = login_response.json()
        access_token = login_response_content['access_token']
        cookies = {"access_token": access_token}

        create_post_data = {
            "title":"test_title",
            "content":"test_content",
        }
        create_response = await ac.post("/posts/", json=create_post_data, cookies=cookies)
        created_content = create_response.json()

        post_id = created_content['id']
        edit_post_content = {
            "title":"edited_test_title",
            "content":"edited_test_content",
        }

        response = await ac.put(f"/posts/{post_id}/edit", json=edit_post_content, cookies=cookies)
        response_content = response.json()

        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert response_content['title'] == "edited_test_title", "제목이 수정되어야 한다"
        assert response_content['content'] == "edited_test_content", "내용이 수정되어야 한다"

# 게시글 삭제
@pytest.mark.posts
async def test_delete_post():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username": "test_user_name",
            "email": "test_email@test.com",
            "password": "test_Password_1!",
        }
        await ac.post("/users/signup", json=signup_user)
        login_response = await ac.post("/users/login", json={"email": signup_user["email"], "password": signup_user["password"]})
        login_response_content = login_response.json()
        access_token = login_response_content['access_token']
        cookies = {"access_token": access_token}

        create_post_data = {
            "title":"test_title",
            "content":"test_content",
        }
        create_response = await ac.post("/posts/", json=create_post_data, cookies=cookies)
        created_content = create_response.json()

        post_id = created_content['id']
        
        response = await ac.delete(f"/posts/{post_id}")
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert response.json()['deleted_id'] == post_id, "삭제된 게시글의 id를 반환해야 한다"

# 게시글 목록
@pytest.mark.asyncio
@pytest.mark.posts
async def test_get_posts():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username": "test_user_name",
            "email": "test_email@test.com",
            "password": "test_Password_1!",
        }
        await ac.post("/users/signup", json=signup_user)
        login_response = await ac.post("/users/login", json={"email": signup_user["email"], "password": signup_user["password"]})
        login_response_content = login_response.json()
        access_token = login_response_content['access_token']
        cookies = {"access_token": access_token}

        create_post_data = {
            "title":"test_title_for_get_post",
            "content":"test_content_for_get_post",
        }
        await ac.post("/posts/", json=create_post_data, cookies=cookies)

        response = await ac.get("/posts/")

        response_content = response.json()
        assert response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert isinstance(response_content['posts'], list), "게시글 목록을 반환해야 한다"

        created_at_response = await ac.get("/posts/?sort_option=created_at")
        created_at_response_content = created_at_response.json()
        assert isinstance(created_at_response_content['posts'], list), "게시글 목록을 반환해야 한다"

        view_count_response = await ac.get("/posts/?sort_option=view_count")
        view_count_response_content = view_count_response.json()
        assert isinstance(view_count_response_content['posts'], list), "게시글 목록을 반환해야 한다"


# 게시글 조회
@pytest.mark.posts
async def test_get_post():
    async with AsyncClient(base_url=BASE_URL) as ac:
        signup_user = {
            "username": "test_user_name",
            "email": "test_email@test.com",
            "password": "test_Password_1!",
        }
        await ac.post("/users/signup", json=signup_user)
        login_response = await ac.post("/users/login", json={"email": signup_user["email"], "password": signup_user["password"]})
        login_response_content = login_response.json()
        access_token = login_response_content['access_token']
        cookies = {"access_token": access_token}

        create_post_data = {
            "title":"test_title_for_get_post",
            "content":"test_content_for_get_post",
        }
        create_response = await ac.post("/posts/", json=create_post_data, cookies=cookies)
        created_content = create_response.json()
        post_id = created_content['id']

        # 게시글 조회 테스트
        get_post_response = await ac.get(f"/posts/{post_id}")
        get_post_content = get_post_response.json()
        assert get_post_response.status_code == 200, "상태코드 200을 반환해야 한다"
        assert get_post_content['title'] == "test_title_for_get_post", "제목이 일치해야 한다"
        assert get_post_content['content'] == "test_content_for_get_post", "내용이 일치해야 한다"

        # 게시글 조회시 조회수 증가 테스트
        check_response = await ac.get("/posts/")
        check_response_content:dict = check_response.json()
        filterd = list(filter(lambda post: post['id'] == post_id, check_response_content.get('posts')))
        assert filterd[0]['view_count'] == 1, "조회수가 증가해야 한다"

# https://medium.com/lseg-developer-community/getting-start-unit-test-with-pytest-for-http-rest-python-application-8bb59eae4d0d

# 탈퇴한 회원이 작성한 포스트는 탈퇴한 회원이라 나와야 한다(회원삭제 구현해야 함)