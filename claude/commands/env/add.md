---
description: 환경변수(DB 접속정보, API 토큰) 추가
allowed-tools: Read, Write, Edit, AskUserQuestion
---

# 환경변수 추가

~/.claude/.env 파일에 DB 접속정보 또는 API 토큰을 추가합니다.

## 사용법

```
/env:add db {PREFIX}      # DB 접속정보 추가
/env:add token {PREFIX}   # API 토큰 추가
```

## 인자

$ARGUMENTS

---

## 처리 흐름

### 1단계: 인자 파싱

```
인자 형식: {type} {prefix}
- type: db | token
- prefix: 대문자 영문 (예: ERP, PORTAL, SLACK)
```

**인자가 없거나 부족한 경우:**
```
"어떤 타입을 추가할까요?"
  ○ db - 데이터베이스 접속정보
  ○ token - API 토큰

"PREFIX를 입력하세요 (대문자 영문):"
→ ERP2
```

---

### 2단계: 정보 입력

**DB 타입인 경우:**

```
"DB 타입을 선택하세요:"
  ○ mssql - Microsoft SQL Server
  ○ mysql - MySQL / MariaDB
  ○ postgres - PostgreSQL

"호스트를 입력하세요:"
→ 192.168.1.100

"포트를 입력하세요:" (기본값 제시)
  - mssql: 1433
  - mysql: 3306
  - postgres: 5432
→ 3306

"데이터베이스명을 입력하세요:"
→ MyDatabase

"사용자명을 입력하세요:"
→ admin

"비밀번호를 입력하세요:"
→ mypassword

"추가 옵션이 있나요? (없으면 엔터):"
→ (선택사항)
```

**Token 타입인 경우:**

```
"토큰 값을 입력하세요:"
→ xoxb-xxxxx-xxxxx
```

---

### 3단계: .env 파일에 추가

**DB 형식:**
```bash
# {PREFIX} Database ({DB_TYPE})
{PREFIX}_DB_TYPE={type}
{PREFIX}_DB_HOST={host}
{PREFIX}_DB_PORT={port}
{PREFIX}_DB_NAME={dbname}
{PREFIX}_DB_USER={user}
{PREFIX}_DB_PASSWORD={password}
{PREFIX}_DB_OPTIONS={options}  # 있는 경우만
```

**Token 형식:**
```bash
# {PREFIX} API Token
{PREFIX}_API_TOKEN={value}
```

---

### 4단계: 완료 안내

```
✅ 환경변수 추가 완료!

추가된 항목:
┌─────────────────────────────────────┐
│ PREFIX: ERP2                        │
│ TYPE:   db (mssql)                  │
│ HOST:   192.168.1.100               │
│ PORT:   1433                        │
│ DBNAME: MyDatabase                  │
└─────────────────────────────────────┘

사용법: /db:query ERP2 "SELECT * FROM table"
```

---

## 예시

### DB 추가

```
/env:add db PORTAL

→ "DB 타입을 선택하세요:"
  ● mysql

→ "호스트를 입력하세요:"
  192.168.1.50

→ "포트를 입력하세요: (기본값: 3306)"
  3306

→ "데이터베이스명을 입력하세요:"
  PortalDB

→ "사용자명을 입력하세요:"
  portal_user

→ "비밀번호를 입력하세요:"
  ********

→ ✅ PORTAL_DB_* 추가 완료!
```

### 토큰 추가

```
/env:add token SLACK

→ "토큰 값을 입력하세요:"
  xoxb-123456789

→ ✅ SLACK_API_TOKEN 추가 완료!
```

---

## 주의사항

- PREFIX는 대문자 영문만 허용
- 이미 존재하는 PREFIX는 덮어쓰기 확인
- .env 파일은 git에 커밋하지 않음 (민감정보)
