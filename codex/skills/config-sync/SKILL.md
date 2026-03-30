---
name: config-sync
description: 원격에서 AI 에이전트 설정을 pull하고 Claude/Codex 링크 상태를 점검하거나 보정할 때 사용한다. Claude의 `/config:sync` 명령을 Codex에서 같은 의미로 수행할 때 대응 매핑으로 사용한다.
---

# Config Sync

## 언제 사용하나

- 원격 저장소에서 `ai-agent-config` 최신 변경을 가져와야 할 때
- Claude와 Codex 설정 링크가 정상인지 같이 확인해야 할 때
- Claude의 `/config:sync`를 Codex에서 같은 의도로 수행해야 할 때

## source mapping

- Claude command: `/config:sync`
- Source file: `claude/commands/config/sync.md`

## 기본 규칙

- source command의 의도를 유지한다.
- 원격 저장소 pull 이후 Codex 링크 상태를 점검한다.
- 누락된 심볼릭 링크만 보정하고, 기존 정상 링크는 불필요하게 건드리지 않는다.
- 사용자가 같은 동작을 요청하면 아래 source workflow를 기준으로 수행한다.

## source workflow

# Config Sync

원격 저장소에서 최신 설정을 가져오고, Claude와 Codex에 동기화합니다.

## 실행 흐름

### 1단계: 원격에서 Pull

```bash
cd ~/.ai-agent-config && git pull
```

### 2단계: Codex 스킬 동기화 확인

Codex 심볼릭 링크 상태 확인:

```bash
# skills 폴더 확인
ls -la ~/.codex/skills 2>/dev/null || echo "skills not linked"

# AGENTS.md 확인
ls -la ~/.codex/AGENTS.md 2>/dev/null || echo "AGENTS.md not linked"
```

### 3단계: 누락된 링크 생성 (필요시)

```bash
# skills 폴더 링크 (없으면 생성)
[ ! -L ~/.codex/skills ] && ln -sf ~/.ai-agent-config/codex/skills ~/.codex/skills

# AGENTS.md 링크 (없으면 생성)
[ ! -L ~/.codex/AGENTS.md ] && ln -sf ~/.ai-agent-config/codex/AGENTS.md ~/.codex/AGENTS.md
```

## 결과 표시

```
═══════════════════════════════════════════════════════════════
                      동기화 결과
═══════════════════════════════════════════════════════════════

■ Git Pull
┌─────────────────────────────────────────────────────────────┐
│ {업데이트된 파일 목록 또는 "Already up to date."}            │
└─────────────────────────────────────────────────────────────┘

■ Claude 설정
│ commands/  → 심볼릭 링크 ✓
│ skills/    → 심볼릭 링크 ✓
│ CLAUDE.md  → 심볼릭 링크 ✓

■ Codex 설정
│ skills/    → 심볼릭 링크 ✓
│ AGENTS.md  → 심볼릭 링크 ✓

═══════════════════════════════════════════════════════════════
```

## 참조

- 동기화 구조: `~/.claude/skills/sync-config/skill.md`
