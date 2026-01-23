---
description: Claude ↔ Codex 간 환경변수(.env) 동기화
allowed-tools: Bash(ln:*), Bash(ls:*), Bash(mv:*), Read
---

# 환경변수 동기화

Claude와 Codex 간 `.env` 파일을 심볼릭 링크로 공유합니다.

## 사용법

```
/env:sync codex      # Claude → Codex (.env 공유)
/env:sync            # 상태 확인
```

## 인자

$ARGUMENTS

---

## 처리 흐름

### 인자 없음: 상태 확인

```bash
echo "=== .env 동기화 상태 ==="
ls -la ~/.claude/.env 2>/dev/null || echo "Claude: .env 없음"
ls -la ~/.codex/.env 2>/dev/null || echo "Codex: .env 없음"
```

**출력:**
```
═══════════════════════════════════════════════════════════════
                    .env 동기화 상태
═══════════════════════════════════════════════════════════════

■ Claude
│ ~/.claude/.env → 파일 존재 ✓

■ Codex
│ ~/.codex/.env → ~/.claude/.env (심볼릭 링크) ✓

═══════════════════════════════════════════════════════════════
```

---

### `codex` 인자: 심볼릭 링크 생성

**1단계: Claude .env 확인**

```bash
if [ ! -f ~/.claude/.env ]; then
    echo "Error: ~/.claude/.env 파일이 없습니다."
    echo "먼저 /env:add로 환경변수를 추가하세요."
    exit 1
fi
```

**2단계: 기존 Codex .env 백업**

```bash
if [ -f ~/.codex/.env ] && [ ! -L ~/.codex/.env ]; then
    mv ~/.codex/.env ~/.codex/.env.bak
    echo "기존 .env 백업: ~/.codex/.env.bak"
fi
```

**3단계: 심볼릭 링크 생성**

```bash
ln -sf ~/.claude/.env ~/.codex/.env
```

**4단계: 확인**

```bash
ls -la ~/.codex/.env
```

**출력:**
```
✅ 동기화 완료!

~/.codex/.env → ~/.claude/.env (심볼릭 링크)

이제 Codex에서도 동일한 환경변수를 사용합니다:
- DB 접속정보: {PREFIX}_DB_*
- API 토큰: {PREFIX}_API_TOKEN
```

---

## 예시

### 상태 확인

```
/env:sync

═══════════════════════════════════════════════════════════════
                    .env 동기화 상태
═══════════════════════════════════════════════════════════════

■ Claude
│ ~/.claude/.env → 파일 존재 ✓ (3개 항목)

■ Codex
│ ~/.codex/.env → 링크 없음 ⚠️

💡 동기화하려면: /env:sync codex

═══════════════════════════════════════════════════════════════
```

### 동기화 실행

```
/env:sync codex

✅ 동기화 완료!

~/.codex/.env → ~/.claude/.env (심볼릭 링크)

공유되는 환경변수:
┌──────────┬─────────┐
│ PREFIX   │ TYPE    │
├──────────┼─────────┤
│ ERP      │ db      │
│ AZURE    │ db      │
│ DOORAY   │ token   │
└──────────┴─────────┘
```

---

## 주의사항

- Claude의 `.env`가 원본, Codex는 링크
- `.env` 수정은 어느 쪽에서 해도 동일 파일
- git에 커밋되지 않음 (민감정보)

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/env:add` | 환경변수 추가 |
| `/env:list` | 환경변수 목록 |
| `/env:remove` | 환경변수 삭제 |
