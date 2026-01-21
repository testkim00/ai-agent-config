---
description: 등록된 환경변수(DB, 토큰) 삭제
allowed-tools: Read, Write, Edit, AskUserQuestion
---

# 환경변수 삭제

~/.claude/.env 파일에서 DB 접속정보 또는 API 토큰을 삭제합니다.

## 사용법

```
/env:remove db {PREFIX}      # DB 접속정보 삭제
/env:remove token {PREFIX}   # API 토큰 삭제
```

## 인자

$ARGUMENTS

---

## 처리 흐름

### 1단계: 인자 파싱

```
인자 형식: {type} {prefix}
- type: db | token
- prefix: 삭제할 PREFIX (예: ERP, PORTAL, SLACK)
```

**인자가 없거나 부족한 경우:**
```
"어떤 타입을 삭제할까요?"
  ○ db - 데이터베이스 접속정보
  ○ token - API 토큰

"삭제할 PREFIX를 선택하세요:"
  ○ ERP
  ○ PORTAL
  ○ Other (직접 입력)
```

---

### 2단계: 존재 확인

**DB 타입:**
- `{PREFIX}_DB_TYPE` 키가 존재하는지 확인
- 없으면 에러: "ERP2_DB_* 항목을 찾을 수 없습니다."

**Token 타입:**
- `{PREFIX}_API_TOKEN` 키가 존재하는지 확인
- 없으면 에러: "SLACK_API_TOKEN 항목을 찾을 수 없습니다."

---

### 3단계: 삭제 확인

```
⚠️ 다음 항목을 삭제합니다:

┌─────────────────────────────────────┐
│ PREFIX: ERP                         │
│ TYPE:   db (mssql)                  │
│ HOST:   121.156.75.143              │
│ PORT:   1433                        │
│ DBNAME: WERPBiz                     │
└─────────────────────────────────────┘

"정말 삭제하시겠습니까?"
  ○ Yes - 삭제
  ○ No - 취소
```

---

### 4단계: .env 파일에서 삭제

**DB 삭제 대상:**
```bash
# 주석 포함 삭제
# {PREFIX} Database (...)
{PREFIX}_DB_TYPE=...
{PREFIX}_DB_HOST=...
{PREFIX}_DB_PORT=...
{PREFIX}_DB_NAME=...
{PREFIX}_DB_USER=...
{PREFIX}_DB_PASSWORD=...
{PREFIX}_DB_OPTIONS=...  # 있는 경우
```

**Token 삭제 대상:**
```bash
# 주석 포함 삭제
# {PREFIX} API Token
{PREFIX}_API_TOKEN=...
```

---

### 5단계: 완료 안내

```
✅ 환경변수 삭제 완료!

삭제된 항목: ERP_DB_* (mssql)
```

---

## 예시

### DB 삭제

```
/env:remove db PORTAL

→ ⚠️ 다음 항목을 삭제합니다:
  ┌─────────────────────────────────────┐
  │ PREFIX: PORTAL                      │
  │ TYPE:   mysql                       │
  │ HOST:   192.168.1.50                │
  └─────────────────────────────────────┘

→ "정말 삭제하시겠습니까?"
  ● Yes

→ ✅ PORTAL_DB_* 삭제 완료!
```

### 토큰 삭제

```
/env:remove token SLACK

→ ⚠️ 다음 항목을 삭제합니다:
  ┌─────────────────────────────────────┐
  │ PREFIX: SLACK                       │
  │ VALUE:  xoxb-******                 │
  └─────────────────────────────────────┘

→ "정말 삭제하시겠습니까?"
  ● Yes

→ ✅ SLACK_API_TOKEN 삭제 완료!
```

---

## 주의사항

- 삭제 전 반드시 확인 프롬프트 표시
- 삭제된 데이터는 복구 불가
- 잘못 삭제 시 `/env:add`로 다시 추가

---

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/env:add` | 환경변수 추가 |
| `/env:list` | 환경변수 목록 |
