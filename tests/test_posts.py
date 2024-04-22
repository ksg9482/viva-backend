from fastapi import HTTPException
import pytest
from unittest.mock import AsyncMock
from src.posts.services import PostService
from src.posts.models import Post, PostSortEnum, PostView
from src.posts.repository import PostRepository
from src.users.models import User

@pytest.fixture
def post_repository():
    post_repository = PostRepository()

    post_repository.save = AsyncMock()
    post_repository.find_post_by_id = AsyncMock()
    post_repository.get_post_detail = AsyncMock()
    post_repository.update = AsyncMock()
    post_repository.find_all = AsyncMock()
    post_repository.delete = AsyncMock()

    return post_repository

@pytest.fixture
def post_service(post_repository):
    return PostService(post_repository)

@pytest.mark.unit
@pytest.mark.posts
async def test_create_post(post_service, post_repository):
    user_id = 1
    title = "test_title"
    content = "test_content"
    new_post_view = PostView()
    new_post = Post(user_id=user_id, title=title, content=content, post_view=new_post_view)

    post_repository.save.return_value = new_post

    result = await post_service.create_post(user_id, title, content)

    assert result.title == "test_title", "게시글 제목이 반환되어야 한다."
    assert result.content == "test_content", "게시글 내용이 반환되어야 한다."

@pytest.mark.unit
@pytest.mark.posts
async def test_update_post(post_service, post_repository):
    user_id = 1
    post_id = 1
    title = "updated_title"
    content = "updated_content"
    post = Post(user_id=user_id, title="old_title", content="old_content")

    post_repository.find_post_by_id.return_value = post
    post_repository.update.return_value = post

    result = await post_service.update_post(user_id, post_id, title, content)

    assert result.title == "updated_title", "수정된 게시글 제목이 반환되어야 한다."
    assert result.content == "updated_content", "수정된 게시글 내용이 반환되어야 한다."

@pytest.mark.unit
@pytest.mark.posts
async def test_update_post_not_exist(post_service, post_repository):
    user_id = 1
    post_id = 1
    title = "updated_title"
    content = "updated_content"

    post_repository.find_post_by_id.return_value = None

    with pytest.raises(HTTPException, match="400: 존재하지 않는 포스트입니다."):
        await post_service.update_post(user_id, post_id, title, content)

@pytest.mark.unit
@pytest.mark.posts
async def test_update_post_unauthorized(post_service, post_repository):
    user_id = 1
    post_id = 1
    title = "updated_title"
    content = "updated_content"
    post = Post(user_id=user_id + 1, title="old_title", content="old_content")

    post_repository.find_post_by_id.return_value = post

    with pytest.raises(HTTPException, match="401: 작성자 본인만 수정가능 합니다."):
        await post_service.update_post(user_id, post_id, title, content)

@pytest.mark.unit
@pytest.mark.posts
async def test_delete_post(post_service, post_repository):
    user_id = 1
    post_id = 1
    title = "deleted_test_title"
    content = "deleted_test_content"
    post = Post(user_id=user_id, title=title, content=content)

    post_repository.find_post_by_id.return_value = post
    post_repository.delete.return_value = post

    result = await post_service.delete_post(user_id, post_id)

    assert result.title == "deleted_test_title", "삭제된 게시글 제목이 반환되어야 한다."
    assert result.content == "deleted_test_content", "삭제된 게시글 내용이 반환되어야 한다."

@pytest.mark.unit
@pytest.mark.posts
async def test_delete_post_not_exist(post_service, post_repository):
    user_id = 1
    post_id = 1

    post_repository.find_post_by_id.return_value = None

    with pytest.raises(HTTPException, match="400: 존재하지 않는 포스트입니다."):
        await post_service.delete_post(user_id, post_id)

@pytest.mark.unit
@pytest.mark.posts
async def test_delete_post_unauthorized(post_service, post_repository):
    user_id = 1
    post_id = 1
    title = "test_title"
    content = "test_content"
    post = Post(user_id=user_id + 1, title=title, content=content)

    post_repository.find_post_by_id.return_value = post
    post_repository.delete.return_value = post

    with pytest.raises(HTTPException, match="401: 작성자 본인만 삭제가능 합니다."):
        await post_service.delete_post(user_id, post_id)   

@pytest.mark.unit
@pytest.mark.posts
async def test_get_posts(post_service, post_repository):
    title = "test_title"
    content = "test_content"
    username = "test_user"
    page = 1
    items_per_page = 20
    sort_option = PostSortEnum.CREATED_AT
    user = User(username=username)
    post_view = PostView(view_count=1)
    posts = [Post(user_id=1, title=f"{title}_{i}", content=content, user=user, post_view=post_view) for i in range(items_per_page)]

    post_repository.find_all.return_value = posts

    result = await post_service.get_posts(page, items_per_page, sort_option)

    assert result[0].title == "test_title_0", "게시글 제목이 반환되어야 한다."
    assert result[0].username == "test_user", "작성자의 이름이 반환되어야 한다."
    assert result[0].view_count == 1, "조회수가 반환되어야 한다."

@pytest.mark.unit
@pytest.mark.posts
async def test_get_posts_deleted_user(post_service, post_repository):
    title = "test_title"
    content = "test_content"
    username = "test_user"
    page = 1
    items_per_page = 20
    sort_option = PostSortEnum.CREATED_AT
    deleted_at = "2024-01-01T00:00:00"
    user = User(username=username, deleted_at=deleted_at)
    post_view = PostView()
    posts = [Post(user_id=1, title=f"{title} {i}", content=content, user=user, post_view=post_view) for i in range(items_per_page)]

    post_repository.find_all.return_value = posts

    result = await post_service.get_posts(page, items_per_page, sort_option)

    assert result[0].username == "탈퇴한 유저", "deleted_at에 값이 있는 탈퇴한 유저의 경우 '탈퇴한 유저'로 반환되어야 한다."

@pytest.mark.unit
@pytest.mark.posts
async def test_get_post(post_service, post_repository):
    user_id = 1
    post_id = 1
    title = "test_title"
    content = "test_content"
    username = "test_user"
    created_at = "2024-01-01T00:00:00"
    updated_at = ""
    user = User(username=username)
    post = Post(user_id=user_id, title=title, content=content, user=user, created_at=created_at, updated_at=updated_at)

    post_repository.get_post_detail.return_value = post

    result = await post_service.get_post(post_id)

    assert result.title == "test_title", "게시글 제목이 반환되어야 한다."
    assert result.username == "test_user", "작성자의 이름이 반환되어야 한다."
    assert result.content == "test_content", "게시글 내용이 반환되어야 한다."
    assert result.created_at == "2024-01-01T00:00:00", "게시글 생성일이 반환되어야 한다."
    assert result.updated_at == "", "게시글 수정일이 반환되어야 한다."

@pytest.mark.unit
@pytest.mark.posts
async def test_get_post_not_exist(post_service, post_repository):
    post_id = 1
    
    post_repository.get_post_detail.return_value = None

    with pytest.raises(HTTPException, match="400: 존재하지 않는 포스트입니다."):
        await post_service.get_post(post_id)