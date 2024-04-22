# 비바이노베이션 개발팀 서버파트 사전과제

### JWT
JWT로 Access Token과 Refresh Token을 생성하고 검증하는 auth를 미들웨어를 구성했습니다.
작성자 또는 회원 본인이 아니면 수정/삭제 할 수 없는 부분은 미들웨어를 통해 본인을 검증하도록 하였고, 회원만 가능한 요청과 비회원도 가능한 요청을 구분하여 비회원도 가능한 요청은 토큰 검사 없이 auth를 통과합니다. 

Refresh Token토큰은 생성시 DB에 저장해 Access Token 갱신 때 참조합니다.

### Layerd Architecture
Router(Controller) - Service - Repository로 구성된 레이어 구조를 채택했습니다.

Pydantic을 이용하여 요청 정합성 검사와 응답 직렬화를 구현했고, Service가 도메인 객체를 반환하면 Pydantic의 response_model로 제어합니다. Service가 도메인 객체를 반환하면 router에서 응답을 위한 가공을 하는 것이 service의 사용성을 높이고 각 레이어의 관심사에 더 집중할 수 있는 방법이라고 보았습니다.

### 회원 탈퇴
회원 탈퇴는 DELETE 메서드 대신 PUT 메서드를 이용했습니다. DELETE 메서드를 이용해서 비밀번호를 전송하는 것은 방법이 제한되기 때문에 PUT 메서드의 Body에 비밀번호를 입력하여 전송하는 방식으로 구현했습니다. 

PUT을 선택한 이유는 delete_at에 값을 추가하는 soft delete 방식으로 회원 탈퇴를 구현했기에 POST보다 PUT이 의미의 간극이 더 좁다는 판단이 있었습니다.

### 게시글 작성시 이모지 
DB연결시 charset(charset=utf8mb4)을 설정하여 이모지가 정상적으로 유니코드 변환이 되도록 했습니다. 

### 게시글 목록 정렬과 페이지네이션
게시글 목록의 정렬방식은 Query Parameter를 이용했고 Enum으로 받을 수 있는 값을 제한 했습니다.
* 조회수순: sort_option=view_count
* 작성일순: sort_option=created_at

페이지네이션은 20건으로 두었고 page를 입력하지 않아도 페이지네이션 기준으로 동작하도록 page는 기본값 1을 적용 했습니다. 

### 유닛테스트
유닛테스트는 비즈니스 로직을 위임한 Service 레이어에 대해 작성 했습니다. Repository와 일부 함수를 Mocking하여 Service 메서드를 최대한 독립적으로 테스트 할 수 있게 구성했으나 내부에서 동작하는 함수가 Service 메서드의 중요한 부분을 차지할 경우 Mocking하지 않고 변화가 반영된 값을 검증하도록 했습니다.
* pytest 이용