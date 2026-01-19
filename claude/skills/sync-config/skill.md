# Sync Config Skill

`~/.claude`와 `~/.ai-agent-config` 간의 동기화를 담당하는 공통 모듈입니다.

## 디렉토리 구조

```
~/.claude/
├── commands/  → ~/.ai-agent-config/claude/commands (심볼릭 링크)
├── skills/    → ~/.ai-agent-config/claude/skills (심볼릭 링크)
└── Claude.md  → ~/.ai-agent-config/claude/CLAUDE.md (수동 복사 필요)

~/.ai-agent-config/  → ~/Projects/ai-agent-config (심볼릭 링크)
└── .git/  (원격: github.com/testkim00/ai-agent-config)
```

## 동기화 대상

| 파일/폴더 | 유형 | 동기화 방법 |
|-----------|------|-------------|
| `commands/` | 심볼릭 링크 | 자동 반영 |
| `skills/` | 심볼릭 링크 | 자동 반영 |
| `Claude.md` | 일반 파일 | `sync_claude_md` 호출 |

## 동기화 함수

### sync_claude_md

CLAUDE.md를 ai-agent-config로 복사:

```bash
cp ~/.claude/Claude.md ~/.ai-agent-config/claude/CLAUDE.md
```

### sync_check

동기화 상태 확인:

```bash
cd ~/.ai-agent-config && git status --short
```

### sync_push

변경사항 커밋 및 푸시:

```bash
cd ~/.ai-agent-config && git add -A && git commit -m "{메시지}" && git push
```

## 사용 예시

다른 커맨드/스킬에서 참조:

```markdown
동기화가 필요한 경우 `~/.claude/skills/sync-config/skill.md` 참조하여 처리:

1. CLAUDE.md 수정 시: `sync_claude_md` 실행
2. 변경사항 확인: `sync_check` 실행
3. 원격 푸시: `sync_push` 실행
```

## 참조하는 커맨드

- `/config:push` - 설정 변경사항 푸시
- `/config:sync` - 원격에서 설정 동기화
- `/tidy:md` - 마크다운 정리 후 동기화
