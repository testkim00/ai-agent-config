# Dooray Skill

두레이 API를 활용한 메신저 연동 스킬입니다.

## 환경변수

```bash
# ~/.claude/.env
DOORAY_API_TOKEN=ovnajsg41vuv:xS6NGBIcSeWxYSd-lN2e6g
```

## API 기본 정보

| 항목 | 값 |
|------|-----|
| Base URL | `https://api.dooray.com` |
| 인증 헤더 | `Authorization: dooray-api {토큰}` |
| Content-Type | `application/json` |

## 핵심 API

### 다이렉트 메시지 전송

```bash
POST https://api.dooray.com/messenger/v1/channels/direct-send
Content-Type: application/json

{
    "text": "메시지 내용",
    "organizationMemberId": "멤버ID"
}
```

### 채널에 메시지 전송 (리치 메시지 지원)

```bash
POST https://api.dooray.com/messenger/v1/channels/{channelId}/logs
Content-Type: application/json

{
    "text": "메시지 내용",
    "attachments": [
        {
            "title": "제목",
            "titleLink": "https://...",
            "color": "#36a64f",
            "text": "본문 내용",
            "fields": [
                {"title": "필드명", "value": "값", "short": true}
            ],
            "footer": "푸터 텍스트"
        }
    ]
}
```

> **참고**: 메신저에 직접 파일 업로드 API는 없음. 드라이브 업로드 후 링크 공유 또는 리치 메시지(attachments) 사용.

### 멤버 검색 (공식 API)

```bash
# userCode로 검색
GET https://api.dooray.com/common/v1/members?userCode=kbs

# 이름으로 검색
GET https://api.dooray.com/common/v1/members?name=김범수
```

응답:
```json
{
  "header": {"isSuccessful": true},
  "result": [{
    "id": "3274718546994262997",
    "name": "김범수",
    "userCode": "kbs",
    "externalEmailAddress": "kbs@woorihom.com"
  }]
}
```

> **참고**: `externalEmailAddress` 파라미터는 지원되지 않음. 이메일 검색 시 `@` 앞부분 추출 후 `userCode`로 검색

### 멤버 상세 조회

```bash
GET https://api.dooray.com/common/v1/members/{memberId}
```

응답:
```json
{
  "result": {
    "id": "3274718546994262997",
    "name": "김범수",
    "userCode": "kbs",
    "externalEmailAddress": "kbs@woorihom.com"
  }
}
```

### 채널 목록 조회

```bash
GET https://api.dooray.com/messenger/v1/channels
```

## 데이터 파일

| 파일 | 설명 |
|------|------|
| `~/Projects/company-data/본사직원.json` | 본사 직원 목록 (dooray_member_id 포함) |
| `~/Projects/company-data/dooray_members.json` | 두레이 멤버 ID 매핑 (채널 참가자 기준) |

## 사용자 매핑

| 필드 | ERP | 두레이 |
|------|-----|--------|
| 이름 | emp_name | name |
| 사용자ID | user_id | userCode 또는 externalEmailAddress 앞부분 |
| 멤버ID | dooray_member_id | organizationMemberId |

## Python 구현

### .env 파일 읽기

```python
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

env = load_env()
TOKEN = env.get('DOORAY_API_TOKEN')
```

### 직원 조회 (본사직원.json)

```python
import json

def find_employee(name_or_id_or_email, dept=None):
    """이름, user_id, 또는 이메일로 직원 찾기"""
    path = os.path.expanduser('~/Projects/company-data/본사직원.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 이메일인 경우 user_id 추출
    search_key = name_or_id_or_email
    if '@' in name_or_id_or_email:
        search_key = name_or_id_or_email.split('@')[0]

    matches = []
    for emp in data['employees']:
        if (emp['name'] == search_key or
            emp.get('user_id') == search_key or
            emp.get('user_id') == name_or_id_or_email.split('@')[0]):
            matches.append(emp)

    if not matches:
        return None, "직원을 찾을 수 없습니다"

    if len(matches) == 1:
        return matches[0], None

    # 동명이인 처리
    if dept:
        for m in matches:
            if m.get('dept') == dept:
                return m, None
        return None, f"해당 부서({dept})에 직원이 없습니다"

    # 선택 필요
    return matches, "동명이인"
```

> **이메일 검색**: `kbs@woorihom.co.kr` → `kbs`로 변환하여 user_id와 매칭

### 메시지 전송

```python
import urllib.request
import json

def send_message(member_id, text):
    """두레이 다이렉트 메시지 전송"""
    url = "https://api.dooray.com/messenger/v1/channels/direct-send"
    data = {
        "text": text,
        "organizationMemberId": member_id
    }

    req = urllib.request.Request(url, method='POST')
    req.add_header("Authorization", f"dooray-api {TOKEN}")
    req.add_header("Content-Type", "application/json")
    req.data = json.dumps(data).encode('utf-8')

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))
```

### 전체 흐름

```python
def dooray_messenger(name_or_id, dept=None, message=None):
    """두레이 메신저로 메시지 전송"""
    # 1. 직원 찾기
    result, error = find_employee(name_or_id, dept)

    if error == "동명이인":
        print("동명이인이 있습니다. 부서를 지정해주세요:")
        for emp in result:
            print(f"  - {emp['name']} ({emp.get('dept', '미지정')})")
        return False

    if error:
        print(f"오류: {error}")
        return False

    # 2. 멤버 ID 확인
    member_id = result.get('dooray_member_id')
    if not member_id:
        print(f"두레이 멤버 ID가 없습니다: {result['name']}")
        return False

    # 3. 메시지 전송
    text = message or "세션 출력 내용"  # 실제로는 세션 맥락에서 가져옴
    response = send_message(member_id, text)

    if response.get('header', {}).get('isSuccessful'):
        print(f"메시지 전송 완료: {result['name']}")
        return True
    else:
        print(f"전송 실패: {response}")
        return False
```

## 드라이브 API

### 개인 드라이브 목록 조회

```bash
GET https://api.dooray.com/drive/v1/drives?type=private
```

응답:
```json
{
  "header": {"isSuccessful": true},
  "result": [{
    "id": "123456789",
    "name": "내 드라이브",
    "type": "private"
  }]
}
```

### 폴더/파일 목록 조회

```bash
# root 폴더 조회
GET https://api.dooray.com/drive/v1/drives/{drive-id}/files?parentId=root

# 특정 폴더 하위 조회
GET https://api.dooray.com/drive/v1/drives/{drive-id}/files?parentId={folder-id}

# 폴더만 조회
GET https://api.dooray.com/drive/v1/drives/{drive-id}/files?parentId=root&type=folder

# 파일만 조회 (페이징)
GET https://api.dooray.com/drive/v1/drives/{drive-id}/files?parentId=root&type=file&page=0&size=10
```

### 파일 다운로드

```bash
GET https://api.dooray.com/drive/v1/drives/{drive-id}/files/{file-id}?media=raw
```

> **주의**: 307 리다이렉트 응답. `Location` 헤더의 URL로 재요청 필요.

```bash
# 1. 첫 요청 → 307 응답
curl -I "https://api.dooray.com/drive/v1/drives/123/files/456?media=raw" \
  -H "Authorization: dooray-api {TOKEN}"
# Location: https://file-api.dooray.com/downloads/drive/v1/drives/123/files/456?media=raw

# 2. 리다이렉트 URL로 재요청
curl "https://file-api.dooray.com/downloads/drive/v1/drives/123/files/456?media=raw" \
  -H "Authorization: dooray-api {TOKEN}" -o output.file
```

### 파일 업로드

```bash
POST https://api.dooray.com/drive/v1/drives/{drive-id}/files?parentId={folder-id}
Content-Type: multipart/form-data
```

> **주의**: 307 리다이렉트 방식. 자동 리다이렉트 OFF 필요.

```bash
# 1. 첫 요청 → 307 응답
curl -X POST "https://api.dooray.com/drive/v1/drives/{drive-id}/files?parentId=root" \
  -H "Authorization: dooray-api {TOKEN}" \
  -F "file=@/path/to/file.png" \
  --include
# Location: https://file-api.dooray.com/uploads/drive/v1/drives/{drive-id}/files?parentId=root

# 2. 리다이렉트 URL로 재요청 (Authorization, 파일 정보 포함!)
curl -X POST "https://file-api.dooray.com/uploads/drive/v1/drives/{drive-id}/files?parentId=root" \
  -H "Authorization: dooray-api {TOKEN}" \
  -F "file=@/path/to/file.png;filename=file.png;type=image/png"
```

응답:
```json
{"header":{"isSuccessful":true},"result":{"id":"업로드된파일ID"}}
```

### 파일 수정 (덮어쓰기)

```bash
PUT https://api.dooray.com/drive/v1/drives/{drive-id}/files/{file-id}?media=raw
```

> 업로드와 동일하게 307 리다이렉트 방식

## 프로젝트/위키 파일 API

### 업무에 첨부파일 업로드

```bash
POST https://api.dooray.com/project/v1/projects/{project-id}/posts/{post-id}/files
```

### 업무 첨부파일 다운로드

```bash
GET https://api.dooray.com/project/v1/projects/{project-id}/posts/{post-id}/files
```

### 위키 페이지에 파일 업로드

```bash
POST https://api.dooray.com/wiki/v1/wikis/{wiki-id}/pages/{page-id}/files
```

> **모든 파일 업로드 API 공통**: 307 리다이렉트 방식. `Location` 헤더 URL로 재요청 시 Authorization 헤더와 파일 정보를 반드시 포함해야 함.

## 파일 공유 프로세스 (드라이브 → 메신저)

메신저에 직접 파일 업로드 API가 없으므로, 드라이브에 업로드 후 링크를 공유합니다.

### 기본 설정

| 항목 | 값 |
|------|-----|
| 기본 드라이브 | 엑셀요청 |
| 기본 폴더 | claude-shared |
| 파일 URL 형식 | `https://woorihom.dooray.com/drive/files/{file-id}` |

### 전체 흐름

```
1. 드라이브 ID 조회 (또는 기본값 사용)
2. 파일 업로드 (307 리다이렉트 방식)
3. 파일 URL 생성
4. 수신자 멤버 ID 조회
5. 리치 메시지로 링크 전송
```

### Python 구현

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

env = load_env()
TOKEN = env.get('DOORAY_API_TOKEN')

# 기본 설정 (엑셀요청 드라이브)
DEFAULT_DRIVE_ID = "{EXCEL_REQUEST_DRIVE_ID}"
DEFAULT_FOLDER_ID = "{CLAUDE_SHARED_FOLDER_ID}"

def upload_file_to_drive(file_path, drive_id=None, folder_id=None):
    """드라이브에 파일 업로드 (307 리다이렉트 방식)"""
    drive_id = drive_id or DEFAULT_DRIVE_ID
    folder_id = folder_id or DEFAULT_FOLDER_ID

    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        file_content = f.read()

    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'
        f'Content-Type: application/octet-stream\r\n\r\n'
    ).encode('utf-8') + file_content + f'\r\n--{boundary}--\r\n'.encode('utf-8')

    # 1단계: 첫 요청
    url = f"https://api.dooray.com/drive/v1/drives/{drive_id}/files?parentId={folder_id}"
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header("Authorization", f"dooray-api {TOKEN}")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 307:
            location = e.headers.get('Location')
            # 2단계: 리다이렉트 URL로 재요청
            req2 = urllib.request.Request(location, data=body, method='POST')
            req2.add_header("Authorization", f"dooray-api {TOKEN}")
            req2.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
            with urllib.request.urlopen(req2) as response2:
                return json.loads(response2.read().decode('utf-8'))
        raise

def send_file_message(member_id, file_id, file_name, description=""):
    """파일 링크를 리치 메시지로 전송"""
    file_url = f"https://woorihom.dooray.com/drive/files/{file_id}"

    message_data = {
        "text": "📎 파일이 공유되었습니다",
        "organizationMemberId": member_id,
        "attachments": [
            {
                "title": file_name,
                "titleLink": file_url,
                "color": "#36a64f",
                "text": description,
                "footer": "Claude Code"
            }
        ]
    }

    url = "https://api.dooray.com/messenger/v1/channels/direct-send"
    req = urllib.request.Request(url, method='POST')
    req.add_header("Authorization", f"dooray-api {TOKEN}")
    req.add_header("Content-Type", "application/json")
    req.data = json.dumps(message_data).encode('utf-8')

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def share_file_to_user(file_path, name_or_id, dept=None, description=""):
    """파일을 드라이브에 업로드하고 사용자에게 링크 전송"""
    # 1. 파일 업로드
    result = upload_file_to_drive(file_path)
    file_id = result['result']['id']
    file_name = result['result']['name']

    # 2. 수신자 찾기
    emp, error = find_employee(name_or_id, dept)
    if error:
        return None, error

    member_id = emp.get('dooray_member_id')
    if not member_id:
        return None, "dooray_member_id 없음"

    # 3. 메시지 전송
    send_result = send_file_message(member_id, file_id, file_name, description)
    return send_result, None
```

## 멤버 ID 갱신

채널 참가자 기반으로 멤버 매핑을 갱신합니다:

```python
def refresh_dooray_members():
    """두레이 멤버 매핑 갱신"""
    # 1. 채널 목록에서 모든 멤버 ID 수집
    url = "https://api.dooray.com/messenger/v1/channels"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"dooray-api {TOKEN}")

    with urllib.request.urlopen(req) as response:
        channels = json.loads(response.read().decode('utf-8'))

    member_ids = set()
    for ch in channels.get('result', []):
        for p in ch.get('users', {}).get('participants', []):
            mid = p.get('member', {}).get('organizationMemberId')
            if mid:
                member_ids.add(mid)

    # 2. 각 멤버 상세 조회
    members = []
    for mid in member_ids:
        url = f"https://api.dooray.com/common/v1/members/{mid}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"dooray-api {TOKEN}")
        try:
            with urllib.request.urlopen(req) as response:
                info = json.loads(response.read().decode('utf-8')).get('result', {})
                email = info.get('externalEmailAddress', '')
                members.append({
                    'name': info.get('name', ''),
                    'user_id': email.split('@')[0] if email else '',
                    'user_code': info.get('userCode', ''),
                    'dooray_member_id': mid
                })
        except:
            pass

    # 3. 저장
    with open(os.path.expanduser('~/Projects/company-data/dooray_members.json'), 'w') as f:
        json.dump({
            'updated_at': '2026-01-17',
            'members': sorted(members, key=lambda x: x['name'])
        }, f, ensure_ascii=False, indent=2)

    return len(members)
```

## 참고 문서

- [Dooray API 개요](https://helpdesk.dooray.com/share/pages/9wWo-xwiR66BO5LGshgVTg/2937064454837487755)
- [메시지 보내기](https://helpdesk.dooray.com/share/pages/9wWo-xwiR66BO5LGshgVTg/2900075337309822215)
- [Messenger API (공식)](https://helpdesk.dooray.com/share/pages/9wWo-xwiR66BO5LGshgVTg/2939992834004986234)
- [드라이브 API 활용 가이드](https://helpdesk.dooray.com/share/pages/9wWo-xwiR66BO5LGshgVTg) - `~/Projects/Dooray드라이브 API 활용 가이드.html`
- [파일 업/다운로드 API 가이드](https://helpdesk.dooray.com/share/pages/9wWo-xwiR66BO5LGshgVTg) - `~/Projects/Dooray파일 업다운로드 관련 API 가이드.html`
