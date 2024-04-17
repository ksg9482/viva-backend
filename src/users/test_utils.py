import jwt
import pytest
from utills import UserUtills

@pytest.mark.utills
def test_encode_token():
    username = "test_user"
    email = "test@test.com"
    token = UserUtills.encode_token(email, username)
    print(token)
    # 토큰은 암호화되어야 한다
    assert token is not None, "토큰이 반환되어야 합니다."

    # username이 None일 때 테스트
    with pytest.raises(ValueError, match="username is None"):
        UserUtills.encode_token(None)

@pytest.mark.utills
def test_decode_token():
    # 유효한 토큰에 대한 테스트
    username = "test_user"
    email = "test@test.com"
    token = UserUtills.encode_token(email, username)

    payload = UserUtills.decode_token(token)
    assert payload['data']['email'] == email, "페이로드는 username을 포함해야 합니다."
    assert payload['data']['username'] == username, "페이로드는 username을 포함해야 합니다."
    
    # 토큰의 유효기간은 1시간이다.
    assert payload['exp'] - payload['iat'] == 3600, "토큰의 유효기간은 1시간이어야 합니다."

    # 유효하지 않은 토큰에 대한 테스트
    invalid_token = token + "invalid"
    result = UserUtills.decode_token(invalid_token)
    assert isinstance(result, jwt.exceptions.InvalidTokenError), "유효하지 않은 토큰은 'Invalid token'를 반환해야 합니다."