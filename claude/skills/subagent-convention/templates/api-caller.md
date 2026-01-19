# API Caller Template

API 호출용 subagent 템플릿 (REST, DB 쿼리)

## 템플릿

```python
Task(
    subagent_type="Bash",
    model="sonnet",  # config.md 참조
    prompt="""
    {작업명} API 호출:

    [API 정보]:
    - 엔드포인트: {endpoint}
    - 메서드: {method}
    - 인증: {auth_type}

    [요청 데이터]:
    {request_body}

    [처리 단계]:
    1. 인증 정보 로드
       - {env_file}에서 토큰 읽기

    2. API 호출
       - Python urllib 사용
       - 헤더 설정

    3. 응답 처리
       - 상태 코드 확인
       - 응답 데이터 파싱

    [출력]:
    - API 응답 결과
    - 성공/실패 여부
    - 에러 시 에러 메시지
    """
)
```

## 사용 예시

### REST API 호출

```python
Task(
    subagent_type="Bash",
    model="sonnet",
    prompt="""
    두레이 메시지 전송:

    [API 정보]:
    - 엔드포인트: https://api.dooray.com/messenger/v1/channels/direct-send
    - 메서드: POST
    - 인증: dooray-api {token}

    [요청 데이터]:
    - organizationMemberId: {member_id}
    - text: {message}

    [처리 단계]:
    1. ~/.claude/.env에서 DOORAY_API_TOKEN 로드
    2. 수신자 정보 조회 (본사직원.json)
    3. API 호출
    4. 응답 확인

    [출력]:
    - 전송 성공/실패
    - 수신자 정보
    """
)
```

### DB 쿼리

```python
Task(
    subagent_type="Bash",
    model="sonnet",
    prompt="""
    DB 쿼리 실행:

    [쿼리]:
    {sql_query}

    [출력 형식]: {xlsx/json/console}
    [출력 경로]: {output_path}

    [처리 단계]:
    1. DB 연결 정보 로드
    2. 쿼리 실행 (query.py 사용)
    3. 결과 처리
       - 파일 출력 시 저장
       - 콘솔 출력 시 포맷팅

    [출력]:
    - 조회 건수
    - 출력 파일 경로 (있는 경우)
    - 에러 시 에러 메시지
    """
)
```
