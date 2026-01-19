# AI Agent Config

AI 에이전트(Claude Code, Codex 등)의 공유 설정 저장소

## 설치

```bash
curl -sL https://raw.githubusercontent.com/testkim/ai-agent-config/main/install.sh | bash
```

## 구조

```
ai-agent-config/
├── claude/
│   ├── skills/           # Claude Code 스킬
│   ├── commands/         # Claude Code 커맨드
│   └── CLAUDE.md         # Claude 설정
├── codex/
│   ├── skills/           # Codex 스킬
│   └── AGENTS.md         # Codex 설정
├── install.sh            # 설치 스크립트
├── sync.sh               # 원격에서 동기화
└── push.sh               # 변경사항 푸시
```

## 사용법

### Claude Code에서

```bash
/config:sync    # 원격에서 pull
/config:push    # 변경사항 push
```

### 터미널에서

```bash
~/.ai-agent-config/sync.sh   # 동기화
~/.ai-agent-config/push.sh   # 푸시
```

## 지원 에이전트

| 에이전트 | 설정 위치 | 상태 |
|----------|----------|------|
| Claude Code | `~/.claude/` | ✅ |
| OpenAI Codex | `~/.codex/` | ✅ |
