---
name: tidy-meta
description: Claude command `/tidy:meta` 대응 스킬. Claude의 `/tidy:meta` 명령을 Codex에서 skill로 사용할 때 대응 매핑으로 사용한다.
---

# Tidy Meta

## 언제 사용하나

- Claude command `/tidy:meta` 대응 스킬.
- Claude의 `/tidy:meta`를 Codex에서 같은 의도로 수행해야 할 때

## source mapping

- Claude command: `/tidy:meta`
- Source file: `claude/commands/tidy/meta.md`

## 기본 규칙

- source command의 의도를 유지한다.
- Claude 전용 구문인 `allowed-tools`, `Task`, `AskUserQuestion`은 Codex 실행 환경에 맞게 해석한다.
- 사용자가 같은 동작을 요청하면 아래 source workflow를 기준으로 수행한다.

## source workflow

# Tidy Meta

마스터 메타정보(`_relations.yaml`)를 정리하고 업데이트합니다.

## 사용법

```
/tidy:meta              # 메타정보 검증 및 정리
/tidy:meta scan         # 전체 스캔 후 누락된 관계 제안
/tidy:meta validate     # 유효성 검증만 (수정 없음)
```

## 대상 파일

```
/Users/honeychaser/Projects/ai-agent-config/codex/_relations.yaml
```

## 처리 흐름

### 1. 현황 스캔

```bash
# upstream Claude commands 구조 스캔
ls -R /Users/honeychaser/Projects/ai-agent-config/claude/commands/

# Codex skills 구조 스캔
ls -R /Users/honeychaser/Projects/ai-agent-config/codex/skills/
```

### 2. 유효성 검증

| 검증 항목 | 설명 |
|----------|------|
| 참조 파일 존재 | commands/skills에 명시된 파일이 실제 존재하는지 |
| 고아 파일 | 관계에 포함되지 않은 commands/skills 파일 |
| 중복 정의 | 같은 파일이 여러 관계에 중복 정의 |
| skill_internals | 스킬 내부 파일들의 존재 여부 |

### 3. 정리 수행

**삭제 대상:**
- 존재하지 않는 파일 참조
- 중복 정의된 관계

**추가 제안:**
- 관계에 포함되지 않은 commands/skills
- 새로 생성된 스킬의 내부 구조

### 4. 결과 출력

```
═══════════════════════════════════════════════════════════════
                    메타정보 정리 결과
═══════════════════════════════════════════════════════════════

■ 현황
┌─────────────────────────────────────────────────────────────┐
│ Source Commands: {N}개 폴더, {M}개 파일                      │
│ Codex Skills: {N}개 스킬                                     │
│ 정의된 관계: {N}개                                          │
└─────────────────────────────────────────────────────────────┘

■ 검증 결과
┌──────────────────┬──────────┬───────────────────────────────┐
│ 항목             │ 상태     │ 설명                          │
├──────────────────┼──────────┼───────────────────────────────┤
│ 참조 파일 존재   │ ✅ / ⚠️  │ {상세}                        │
│ 고아 파일        │ ✅ / ⚠️  │ {상세}                        │
│ 중복 정의        │ ✅ / ⚠️  │ {상세}                        │
│ skill_internals  │ ✅ / ⚠️  │ {상세}                        │
└──────────────────┴──────────┴───────────────────────────────┘

■ 수정 내역
┌─────────┬───────────────────────────────────────────────────┐
│ 삭제    │ {삭제된 참조 목록}                                │
│ 추가    │ {추가된 관계 목록}                                │
│ 수정    │ {수정된 항목 목록}                                │
└─────────┴───────────────────────────────────────────────────┘

■ 추가 제안 (수동 검토 필요)
┌─────────────────────────────────────────────────────────────┐
│ 1. {command/skill}이 관계에 포함되지 않음                   │
│    → 추천: relations에 추가 또는 의도적 제외 확인           │
│                                                             │
│ 2. {skill}의 내부 구조가 정의되지 않음                      │
│    → 추천: skill_internals에 추가                           │
└─────────────────────────────────────────────────────────────┘
═══════════════════════════════════════════════════════════════
```

## _relations.yaml 구조

```yaml
# 커맨드-스킬 관계 정의
relations:
  - commands: ["../claude/commands/orchestration.md"]
    skills: ["subagent-convention"]
    description: "5단계 흐름, 위임 체계"

  - commands: ["../claude/commands/git/*.md"]
    skills: ["git-convention"]
    description: "커밋, 브랜치 규칙"

# 그룹 내 공유 파일
shared_files:
  tidy:
    - "../claude/commands/tidy/_common.md"

# 전역 참조
global:
  - "AGENTS.md"
  - "_relations.yaml"

# 스킬 내부 구조
skill_internals:
  subagent-convention:
    - "_index.md"
    - "instruction.md"
    - "config.md"
    - "templates/*.md"
```

## 자동 정리 규칙

| 상황 | 동작 |
|------|------|
| 파일 삭제됨 | 참조 자동 제거 |
| 새 폴더 생성됨 | 관계 추가 제안 |
| 스킬 구조 변경됨 | skill_internals 업데이트 제안 |

## 추가 규칙

- `_relations.yaml` 변경만을 이유로 자동 commit하지 않는다. commit은 사용자가 명시적으로 요청한 경우에만 수행한다.
- 대폭 변경(5개+ 항목) 시 사용자 확인
- validate 모드는 수정 없이 검증만 수행
