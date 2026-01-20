# Config 커맨드 인덱스

> **수정 시 필수 확인**
>
> Config 커맨드 수정 전:
> 1. 이 파일의 관련 문서 목록 확인
> 2. `skills/sync-config/skill.md` 확인
> 3. 심볼릭 링크 구조 이해

## 문서 구조

```
commands/config/
├── _index.md       ← 현재 파일
├── push.md         ← 설정 푸시
└── sync.md         ← 설정 동기화
```

## 커맨드 목록

| 커맨드 | 파일 | 설명 |
|--------|------|------|
| `/config:push` | `push.md` | 설정 변경사항 원격 푸시 |
| `/config:sync` | `sync.md` | 원격 설정 로컬 동기화 |

## 관련 스킬

| 스킬 | 경로 | 역할 |
|------|------|------|
| Sync Config | `skills/sync-config/skill.md` | 동기화 로직 정의 |

## 디렉토리 구조

```
~/.claude/
├── commands/  → ~/.ai-agent-config/claude/commands (심볼릭 링크)
├── skills/    → ~/.ai-agent-config/claude/skills (심볼릭 링크)
└── CLAUDE.md  → ~/.ai-agent-config/claude/CLAUDE.md (심볼릭 링크)

~/.ai-agent-config/  → ~/Projects/ai-agent-config (심볼릭 링크)
└── .git/  (원격: github.com/testkim00/ai-agent-config)
```

## 워크플로우

```
설정 수정
    │
    ▼
/config:push (원격 푸시)

다른 머신에서
    │
    ▼
/config:sync (로컬 동기화)
```

## 수정 시 체크리스트

- [ ] 동기화 대상 변경 → `skill.md`, `push.md`, `sync.md` 함께 수정
- [ ] 원격 저장소 변경 → `skill.md` 수정
