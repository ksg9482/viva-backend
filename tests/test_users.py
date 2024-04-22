from datetime import timedelta
import pytest
from unittest.mock import AsyncMock, Mock, patch
from fastapi import HTTPException
from src.users.services import UserService
from src.users.repository import UserRepository
from src.users.models import RefreshToken, User
from src.auth.utills import JwtUtils
import src.users.dependencies as dependencies

@pytest.fixture
def user_repository():
    user_repository = UserRepository()
    user_repository.find_by_id = AsyncMock()
    user_repository.find_by_email = AsyncMock()
    user_repository.save = AsyncMock()
    user_repository.edit_user = AsyncMock()
    user_repository.delete_soft_user = AsyncMock()
    user_repository.save_refresh_token = AsyncMock()
    return user_repository

@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository)

@pytest.mark.unit
@pytest.mark.users
async def test_create_user_account(user_service, user_repository):
    username = "test_username"
    email = "testuser@example.com"
    password = "test_password"
    user = User(username=username, email=email, password=password)

    user_repository.save.return_value = user
    user_repository.find_by_email.return_value = None

    result = await user_service.create_user_account(username, email, password)

    assert result.username == "test_username", "사용자 이름이 반환되어야 한다."
    assert result.email == "testuser@example.com", "이메일이 반환되어야 한다."
    assert result.password != "test_password", "비밀번호가 해싱되어 반환되어야 한다."

@pytest.mark.unit
@pytest.mark.users
async def test_create_user_duplicate_account(user_service, user_repository):
    username = "test_username"
    email = "testuser@example.com"
    password = "test_password"
    user = User(username=username, email=email, password=password)

    user_repository.save.return_value = user
    user_repository.find_by_email.return_value = user

    with pytest.raises(HTTPException, match='이미 가입된 사용자입니다.'):
        await user_service.create_user_account(username, email, password)

@pytest.mark.unit
@pytest.mark.users
async def test_login(user_service, user_repository):
    email = "testuser@example.com"
    password = "test_password"
    user = User(email=email, password=password)

    user_repository.find_by_email.return_value = user
    user_service.valid_password = Mock(return_value=True)
    user_service.utills.encode_access_token = Mock(return_value="access_token")
    user_service.utills.encode_refresh_token = Mock(return_value="refresh_token")

    result = await user_service.login(email, password)

    user_repository.find_by_email.assert_called_once_with(email)
    assert result.access_token == "access_token", "access_token이 반환되어야 한다."
    assert result.refresh_token == "refresh_token", "refresh_token이 반환되어야 한다."

@pytest.mark.unit
@pytest.mark.users
async def test_login_not_exist_user(user_service, user_repository):
    email = "testuser@example.com"
    password = "test_password"

    user_repository.find_by_email.return_value = None
    with pytest.raises(HTTPException, match='존재하지 않는 사용자입니다.'):
        await user_service.login(email, password)

@pytest.mark.unit
@pytest.mark.users
async def test_login_not_invalid_password(user_service, user_repository):
    email = "testuser@example.com"
    password = "test_password"
    hashed_password = "hashedpassword"
    user = User(email=email, password=hashed_password)

    user_repository.find_by_email.return_value = user
    user_service.valid_password = Mock(return_value=False)

    with pytest.raises(HTTPException, match='잘못된 비밀번호 입니다.'):
        await user_service.login(email, password)

@pytest.mark.unit
@pytest.mark.users
async def test_edit_user(user_service, user_repository):
    id = 1
    password = "old_password"
    username = "updated_username"
    new_password = "updated_password"
    user = User(id=id, username=username, password=password)

    user_service.get_user = AsyncMock(return_value=user)
    user_service.valid_password = Mock(return_value=True)
    user_repository.edit_user.return_value = user

    result = await user_service.edit_user(id, password, username, new_password)
    assert result.username == "updated_username", "사용자 이름이 업데이트 되어야 한다."
    assert result.password != "updated_password" , "업데이트 된 비밀번호가 해싱되어 반환되어야 한다."

@pytest.mark.unit
@pytest.mark.users
async def test_edit_user_invalid_password(user_service):
    id = 1
    password = "old_password"
    username = "updated_username"
    new_password = "updated_password"
    user = User(id=id, username=username, password=password)

    user_service.get_user = AsyncMock(return_value=user)
    user_service.valid_password = Mock(return_value=False)

    with pytest.raises(HTTPException, match='401: 잘못된 비밀번호 입니다.'):
        await user_service.edit_user(id, password, username, new_password)

@pytest.mark.unit
@pytest.mark.users
async def test_delete_user(user_service, user_repository):
    id = 1
    password = "password"
    username = "username"
    user = User(id=id, username=username, password=password)

    user_service.get_user = AsyncMock(return_value=user)
    user_service.valid_password = Mock(return_value=True)
    user_repository.delete_soft_user.return_value = user

    result = await user_service.delete_user(id, password)

    assert result.username == "username", "삭제된 사용자 이름이 반환되어야 한다."
    assert result.deleted_at is not None, "삭제된 사용자의 삭제 시간이 기록되어야 한다."

@pytest.mark.unit
@pytest.mark.users
async def test_delete_user_not_exist_user(user_service, user_repository):
    id = 1
    password = "password"

    user_repository.find_by_id.return_value = None

    with pytest.raises(HTTPException, match='400: 존재하지 않는 사용자입니다.'):
        await user_service.delete_user(id, password)

@pytest.mark.unit
@pytest.mark.users
async def test_delete_user_invalid_password(user_service):
    id = 1
    password = "old_password"
    username = "updated_username"
    new_password = "updated_password"
    user = User(id=id, username=username, password=password)

    user_service.get_user = AsyncMock(return_value=user)
    user_service.valid_password = Mock(return_value=False)

    with pytest.raises(HTTPException, match='401: 잘못된 비밀번호 입니다.'):
        await user_service.edit_user(id, password, username, new_password)

@pytest.mark.unit
@pytest.mark.users
async def test_get_user(user_service, user_repository):
    id = 1
    password = "password"
    username = "username"
    user = User(id=id, username=username, password=password)
    user_repository.find_by_id = AsyncMock(return_value=user)

    result = await user_service.get_user(id)

    assert result.username == "username", "사용자 이름이 반환되어야 한다."

@pytest.mark.unit
@pytest.mark.users
async def test_get_user_not_exist_user(user_service, user_repository):
    id = 1
    user_repository.find_by_id = AsyncMock(return_value=None)

    with pytest.raises(HTTPException, match='400: 존재하지 않는 사용자입니다.'):
        await user_service.get_user(id)

@pytest.mark.unit
@pytest.mark.users
async def test_jwt_refresh(user_service, user_repository):
    access_token = "access_token"
    refresh_token = "refresh_token"
    user_id = 1
    email = "testuser@example.com"
    username = "test_username"
    user = User(id=user_id, email=email, username=username)
    refresh_token = RefreshToken(user_id=user_id, token=refresh_token)

    user_service.utills.encode_access_token = Mock(return_value="new_access_token")
    user_service.utills.encode_refresh_token = Mock(return_value="new_refresh_token")
    user_service.utills.decode_token = Mock(return_value={"data": {"id": user_id}})
    user_repository.find_by_id.return_value = user
    user_repository.save_refresh_token.return_value = refresh_token

    result = await user_service.jwt_refresh(access_token, refresh_token)

    assert result["access_token"] == "new_access_token", "새로운 access_token이 반환되어야 한다."
    assert result["refresh_token"] == "new_refresh_token", "새로운 refresh_token이 반환되어야 한다."

@pytest.mark.unit
@pytest.mark.users
async def test_jwt_refresh_invalid_token(user_service):
    access_token = "invalid_access_token"
    refresh_token = "invalid_refresh_token"

    user_service.utills.decode_token.return_value = None

    with pytest.raises(HTTPException, match="401: 유효하지 않은 토큰입니다."):
        await user_service.jwt_refresh(access_token, refresh_token)

@pytest.mark.unit
async def test_jwt_refresh_not_exist_user(user_service, user_repository):
    user_id = 1

    access_token = "access_token"
    refresh_token = "refresh_token"

    user_service.utills.decode_token = Mock(return_value={"data": {"id": user_id}})
    user_repository.find_by_id.return_value = None

    with pytest.raises(HTTPException, match="400: 존재하지 않는 사용자입니다."):
        await user_service.jwt_refresh(access_token, refresh_token)