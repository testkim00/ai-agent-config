---
description: 원격에서 AI 에이전트 설정 동기화
allowed-tools: Bash(git:*), Bash(ln:*), Bash(cp:*), Bash(ls:*), Bash(mkdir:*)
---

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
