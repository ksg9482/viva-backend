from fastapi import Depends
import jwt
import pytest
from utills import UserUtills, get_user_utills

@pytest.mark.utills
def test_encode_access_token():
    user_id = 1
    username = "test_user"
    email = "test@test.com"
    utills = UserUtills()
    token = utills.encode_access_token(user_id, email, username)
    print(token)
    # 토큰은 암호화되어야 한다
    assert token is not None, "토큰이 반환되어야 한다."

    with pytest.raises(ValueError):
        utills.encode_access_token(None, None, None), "파라미터가 None일 경우 ValueError를 반환해야 한다."

@pytest.mark.utills
def test_decode_token():
    # 유효한 토큰에 대한 테스트
    user_id = 1
    username = "test_user"
    email = "test@test.com"

    utills = UserUtills()
    access_token = utills.encode_access_token(user_id, email, username)
    refresh_token = utills.encode_refresh_token(user_id, email, username)

    access_token_payload = utills.decode_token(access_token)
    assert access_token_payload['data']['id'] == 1, "access_token 페이로드는 id를 포함해야 한다."
    assert access_token_payload['data']['email'] == "test@test.com", "access_token 페이로드는 email을 포함해야 한다."
    assert access_token_payload['data']['username'] == "test_user", "access_token 페이로드는 username을 포함해야 한다."

    refresh_token_payload = utills.decode_token(refresh_token)
    assert refresh_token_payload['data']['id'] == 1, "refresh_token 페이로드는 id를 포함해야 한다."
    assert refresh_token_payload['data']['email'] == "test@test.com", "refresh_token 페이로드는 email을 포함해야 한다."
    assert refresh_token_payload['data']['username'] == "test_user", "refresh_token 페이로드는 username을 포함해야 한다."
    
    # 토큰 유효기간
    assert access_token_payload['exp'] - access_token_payload['iat'] == 3600, "access_token 토큰의 유효기간은 1시간이어야 한다."
    assert refresh_token_payload['exp'] - refresh_token_payload['iat'] == 86400, "refresh_token 토큰의 유효기간은 24시간이어야 한다."

    # 유효하지 않은 토큰에 대한 테스트
    invalid_token = access_token + "invalid"
    result = utills.decode_token(invalid_token)
    assert isinstance(result, jwt.exceptions.InvalidTokenError), "유효하지 않은 토큰은 'Invalid token'를 반환해야 한다."