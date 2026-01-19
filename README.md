# AI Agent Config

AI 에이전트(Claude Code, Codex 등)의 공유 설정 저장소

## 설치

### macOS / Linux

```bash
curl -sL https://raw.githubusercontent.com/testkim00/ai-agent-config/main/install.sh | bash
```

### Windows (PowerShell)

```powershell
git clone https://github.com/testkim00/ai-agent-config.git $env:USERPROFILE\.ai-agent-config
& $env:USERPROFILE\.ai-agent-config\install.ps1
```

> **Note:** 심볼릭 링크 생성을 위해 관리자 권한으로 실행하거나, 개발자 모드를 활성화하세요.

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
├── install.sh            # 설치 스크립트 (macOS/Linux)
├── install.ps1           # 설치 스크립트 (Windows)
├── sync.sh / sync.ps1    # 원격에서 동기화
└── push.sh / push.ps1    # 변경사항 푸시
```

## 사용법

### Claude Code에서

```bash
/config-sync    # 원격에서 pull
/config-push    # 변경사항 push
```

### 터미널에서 (macOS/Linux)

```bash
~/.ai-agent-config/sync.sh   # 동기화
~/.ai-agent-config/push.sh   # 푸시
```

### PowerShell에서 (Windows)

```powershell
& $env:USERPROFILE\.ai-agent-config\sync.ps1   # 동기화
& $env:USERPROFILE\.ai-agent-config\push.ps1   # 푸시
```

## 지원 에이전트

| 에이전트 | 설정 위치 | 상태 |
|----------|----------|------|
| Claude Code | `~/.claude/` | ✅ |
| OpenAI Codex | `~/.codex/` | ✅ |

## 경로 안내

에이전트 설정 디렉토리 위치는 OS와 설치 방식에 따라 다를 수 있습니다.

### Claude Code

| OS | 가능한 경로 |
|----|-------------|
| macOS/Linux | `~/.claude` |
| Windows | `%USERPROFILE%\.claude` |
| Windows | `%APPDATA%\claude` 또는 `%LOCALAPPDATA%\claude` |

### Codex

| OS | 가능한 경로 |
|----|-------------|
| macOS/Linux | `~/.codex` |
| Windows | `%USERPROFILE%\.codex` |
| Windows | `%APPDATA%\codex` 또는 `%LOCALAPPDATA%\codex` |

### 경로 확인 방법

설치 스크립트가 자동으로 탐색하지만, 찾지 못하면 직접 입력할 수 있습니다.

**Windows에서 경로 확인:**
```powershell
# 가능한 경로들 확인
Get-ChildItem -Path $env:USERPROFILE -Filter ".claude" -Directory -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path $env:APPDATA -Filter "claude" -Directory -ErrorAction SilentlyContinue
Get-ChildItem -Path $env:LOCALAPPDATA -Filter "claude" -Directory -ErrorAction SilentlyContinue
```

**AI 에이전트가 설치할 때:**
- 스크립트는 여러 후보 경로를 자동 탐색합니다
- 찾지 못하면 사용자에게 경로 입력을 요청합니다
- 환경에 맞게 적절한 경로를 판단하여 입력하세요
