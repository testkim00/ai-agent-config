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

## Claude vs Codex 스킬 시스템

### Claude Code

Claude Code는 두 가지 스킬 시스템을 사용합니다:

| 시스템 | 경로 | 설명 |
|--------|------|------|
| **plugins** | `~/.claude/plugins/` | 공식 마켓플레이스에서 설치 (자동 업데이트) |
| **skills** | `~/.claude/skills/` | 사용자 정의 스킬 |
| **commands** | `~/.claude/commands/` | 사용자 정의 커맨드 (`/명령어`) |

- `frontend-design`, `document-skills` 등은 **공식 플러그인**으로 제공됨
- 이 저장소의 `claude/skills`는 사용자 정의 스킬만 포함

### Codex

Codex는 플러그인 마켓플레이스가 없습니다:

| 시스템 | 경로 | 설명 |
|--------|------|------|
| **skills** | `~/.codex/skills/` | 모든 스킬 (공식 + 사용자 정의) |
| **AGENTS.md** | `~/.codex/AGENTS.md` | 에이전트 설정 |

- Codex는 `commands` 폴더를 지원하지 않음
- 공식 스킬도 직접 `skills/` 폴더에 넣어야 함

### Codex Command Mapping

Claude의 `/group:name` 커맨드는 Codex에서 직접 지원되지 않으므로, 이 저장소에서는 `group-name` 형식의 skill로 대응합니다.

매핑/동기화 기준 스킬:

- `skill-sync`
  - 경로: `codex/skills/skill-sync/SKILL.md`
  - 역할: `claude/commands/**/*.md`를 전수 검사해서 Codex skill 구조로 대응 매핑

Codex에서 이 매핑 작업 자체를 실행할 때는 `$skill-sync`를 사용합니다.

주의:

- `skill-sync`는 "Claude commands -> Codex skills 매핑" 전용 스킬입니다.
- 기본 동작은 부분 변환이 아니라 전체 command inventory 전수 동기화입니다.
- `config-sync`는 Claude의 원래 `/config:sync` 의미를 그대로 가져온 Codex skill입니다.
- `tidy/_common.md`는 공용 헬퍼이므로 Codex leaf skill 매핑 대상에서 제외합니다.

현재 매핑된 command/skill:

#### Core

| Claude command | Codex skill | 경로 |
|----------------|-------------|------|
| `/analyze:orchestration` | `analyze-orchestration` | `codex/skills/analyze-orchestration/SKILL.md` |
| `/az:swa` | `az-swa` | `codex/skills/az-swa/SKILL.md` |
| `/codex` | `codex` | `codex/skills/codex/SKILL.md` |
| `/consult` | `consult` | `codex/skills/consult/SKILL.md` |
| `/dooray:messenger` | `dooray-messenger` | `codex/skills/dooray-messenger/SKILL.md` |
| `/fix-encoding` | `fix-encoding` | `codex/skills/fix-encoding/SKILL.md` |
| `/orchestration` | `orchestration` | `codex/skills/orchestration/SKILL.md` |

#### Git

| Claude command | Codex skill | 경로 |
|----------------|-------------|------|
| `/git:pr` | `git-pr` | `codex/skills/git-pr/SKILL.md` |
| `/git:save` | `git-save` | `codex/skills/git-save/SKILL.md` |
| `/git:push` | `git-push` | `codex/skills/git-push/SKILL.md` |
| `/git:switch` | `git-switch` | `codex/skills/git-switch/SKILL.md` |
| `/git:sync` | `git-sync` | `codex/skills/git-sync/SKILL.md` |
| `/git:cleanup` | `git-cleanup` | `codex/skills/git-cleanup/SKILL.md` |

#### Config / DB / Env

| Claude command | Codex skill | 경로 |
|----------------|-------------|------|
| `/config:push` | `config-push` | `codex/skills/config-push/SKILL.md` |
| `/config:sync` | `config-sync` | `codex/skills/config-sync/SKILL.md` |
| `/db:convert` | `db-convert` | `codex/skills/db-convert/SKILL.md` |
| `/db:query` | `db-query` | `codex/skills/db-query/SKILL.md` |
| `/env:add` | `env-add` | `codex/skills/env-add/SKILL.md` |
| `/env:list` | `env-list` | `codex/skills/env-list/SKILL.md` |
| `/env:remove` | `env-remove` | `codex/skills/env-remove/SKILL.md` |
| `/env:sync` | `env-sync` | `codex/skills/env-sync/SKILL.md` |

#### Project / Shared / Tidy

| Claude command | Codex skill | 경로 |
|----------------|-------------|------|
| `/project:define` | `project-define` | `codex/skills/project-define/SKILL.md` |
| `/project:memo` | `project-memo` | `codex/skills/project-memo/SKILL.md` |
| `/project:new` | `project-new` | `codex/skills/project-new/SKILL.md` |
| `/project:structure` | `project-structure` | `codex/skills/project-structure/SKILL.md` |
| `/shared:init` | `shared-init` | `codex/skills/shared-init/SKILL.md` |
| `/shared:pull` | `shared-pull` | `codex/skills/shared-pull/SKILL.md` |
| `/shared:push` | `shared-push` | `codex/skills/shared-push/SKILL.md` |
| `/tidy:md` | `tidy-md` | `codex/skills/tidy-md/SKILL.md` |
| `/tidy:meta` | `tidy-meta` | `codex/skills/tidy-meta/SKILL.md` |

보조 git 스킬:

- `git-convention`: 커밋 메시지/브랜치 규칙
- `git-workflow`: 범용 Git 안전 규칙과 작업 절차

### 스킬 공유 구조

```
ai-agent-config/
├── claude/
│   ├── skills/      # 사용자 정의만 (플러그인은 마켓플레이스에서 설치)
│   └── commands/    # 커맨드 지원
├── codex/
│   └── skills/      # 모든 스킬 포함 (플러그인 시스템 없음)
```

두 에이전트를 모두 사용하는 경우, 각각의 스킬 폴더가 독립적으로 관리됩니다.

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
