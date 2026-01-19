# Dooray Messenger 커맨드

세션의 마지막 출력 결과를 두레이 메신저로 전송합니다.

## 사용법

```
/dooray:messenger {사용자}
/dooray:messenger {사용자} {부서}
```

## 입력 결정

| 우선순위 | 조건 | 전송 내용 |
|---------|------|----------|
| 1 | 파이프라인 + 파일 (`$PIPE_INPUT`) | 파일을 드라이브에 업로드 후 링크 전송 |
| 2 | 파이프라인 + 텍스트 | 텍스트 메시지 전송 |
| 3 | 단독 실행 | 세션의 마지막 출력 내용 전송 |

## 파이프라인 예시

```bash
# 쿼리 결과 파일을 업로드 후 링크 전송
/db:query 입사자 현황 > 직원목록.xlsx | /dooray:messenger kbs

# PDF 변환 후 전송
/db:query 월간보고 > 보고서.xlsx | /db:convert pdf | /dooray:messenger 김범수 정보화추진팀
```

- `{사용자}`: 이름(김범수), user_id(kbs), 또는 이메일(kbs@woorihom.co.kr)
- `{부서}`: 동명이인 구분용 (선택사항)

## 예시

```bash
# user_id로 전송
/dooray:messenger kbs

# 이름으로 전송
/dooray:messenger 김범수

# 이메일로 전송
/dooray:messenger kbs@woorihom.co.kr

# 동명이인 구분 (부서 지정)
/dooray:messenger 김범수 정보화추진팀
```

---

# 처리 흐름 (Subagent 활용)

> 모델 설정: `~/.claude/skills/subagent-convention/config.md` 참조

## 역할 분담

| 역할 | 담당 | 작업 |
|------|------|------|
| **판단** | Opus (메인) | 전송 내용 결정, 동명이인 처리 |
| **실행** | Sonnet subagent | 사용자 조회, API 호출, 메시지 전송 |

## Phase 1: 판단 (Opus)

- 전송할 내용 결정 (파일/텍스트)
- 동명이인 있으면 사용자에게 선택 요청

## Phase 2: 메시지 전송 (Sonnet Subagent)

```
Task(
    subagent_type="sonnet",
    model="sonnet",
    prompt="""
    두레이 메시지 전송 작업:

    수신자: {사용자명 또는 ID}
    부서: {부서명 또는 없음}
    전송 내용: {메시지 또는 파일 경로}
    전송 타입: {text/file}

    1. 사용자 조회
       - ~/Projects/company-data/본사직원.json 읽기
       - 이름/user_id/이메일로 검색
       - dooray_member_id 확인

    2. 메시지 전송 (Python urllib 사용)
       - API: POST https://api.dooray.com/messenger/v1/channels/direct-send
       - 헤더: Authorization: dooray-api {토큰}
       - 토큰: ~/.claude/.env의 DOORAY_API_TOKEN

    3. 파일인 경우
       - 드라이브 업로드 먼저
       - 링크 포함하여 전송

    4. 결과 반환
       - 전송 성공/실패
       - 수신자 정보
    """
)
```

## Phase 3: 결과 확인 (Opus)

- 전송 결과 확인
- 사용자에게 응답

## Python 구현

```python
import urllib.request
import json
import os

def load_env(path='~/.claude/.env'):
    env = {}
    with open(os.path.expanduser(path)) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env[key.strip()] = value.strip()
    return env

def find_employee(name_or_id_or_email, dept=None):
    """본사직원.json에서 직원 찾기 (이름, user_id, 이메일 지원)"""
    with open(os.path.expanduser('~/Projects/company-data/본사직원.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 이메일인 경우 user_id 추출
    search_key = name_or_id_or_email
    if '@' in name_or_id_or_email:
        search_key = name_or_id_or_email.split('@')[0]

    matches = []
    for emp in data['employees']:
        if emp['name'] == search_key or emp.get('user_id') == search_key:
            matches.append(emp)

    if not matches:
        return None, "직원을 찾을 수 없습니다"

    if len(matches) == 1:
        return matches[0], None

    # 동명이인 처리
    if dept:
        for m in matches:
            if m['dept'] == dept:
                return m, None
        return None, f"해당 부서({dept})에 직원이 없습니다"

    return matches, "동명이인"

def send_message(member_id, text):
    """두레이 메시지 전송"""
    env = load_env()
    token = env.get('DOORAY_API_TOKEN')

    url = "https://api.dooray.com/messenger/v1/channels/direct-send"
    data = {
        "text": text,
        "organizationMemberId": member_id
    }

    req = urllib.request.Request(url, method='POST')
    req.add_header("Authorization", f"dooray-api {token}")
    req.add_header("Content-Type", "application/json")
    req.data = json.dumps(data).encode('utf-8')

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))
```

## 환경변수

```bash
# ~/.claude/.env
DOORAY_API_TOKEN=xxx:xxx
```

## 데이터 파일

| 파일 | 설명 |
|------|------|
| `~/Projects/company-data/본사직원.json` | 본사 직원 목록 (dooray_member_id 포함) |
| `~/Projects/company-data/dooray_members.json` | 두레이 멤버 ID 매핑 |

## 참고

- [두레이 API 문서](https://helpdesk.dooray.com/share/pages/9wWo-xwiR66BO5LGshgVTg/2937064454837487755)
