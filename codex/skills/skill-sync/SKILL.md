---
name: skill-sync
description: ai-agent-config의 Claude commands를 Codex skills로 대응 매핑하고 동기화할 때 사용한다. 기본 동작은 `claude/commands` 전체를 전수 검사해서 누락 없이 Codex skill로 맞추는 것이다. `/git:pr` 같은 Claude 명령을 `git-pr` 같은 Codex skill로 옮기거나, command frontmatter와 워크플로우를 Codex 실행 규칙에 맞게 번역해야 할 때 사용한다.
---

# Skill Sync

## 목적

`ai-agent-config/claude/commands/**/*.md`에 있는 Claude 전용 command를 `ai-agent-config/codex/skills/<skill-name>/SKILL.md` 형태의 Codex skill로 동기화한다.

여기서 sync는 git pull/push가 아니라 아래 두 축의 대응 매핑을 뜻한다.

- source: Claude command
- target: Codex skill

호출 방식:

- Codex에서는 `$skill-sync`로 호출한다.

주의:

- 이 스킬 이름은 의도적으로 Claude의 `/config:sync`와 구분해서 사용한다.
- 이 스킬은 원격 저장소 pull/push가 아니라 command-to-skill 매핑 작업을 담당한다.

## 기본 범위

- 기본값은 `claude/commands` 전체 전수 검사다.
- 사용자가 특정 그룹만 명시하지 않은 한, 일부 카테고리만 골라서 끝내면 안 된다.
- 완료 보고 전에 source command 목록과 target skill 목록을 다시 비교해서 누락이 `0`인지 검산해야 한다.
- target skill은 파일 존재만으로 완료 처리하지 않는다.
- frontmatter가 깨졌거나 skill 인덱서가 읽지 못하는 상태면 해당 skill은 사실상 누락으로 본다.

## Codex 전용 예외 스킬 목록

- 이 목록은 Claude command를 기계적으로 가져오지 않고, Codex 전용으로 유지할 skill을 뜻한다.
- `$skill-sync`를 사용할 때는 source inventory를 만들기 전에 반드시 이 목록부터 확인한다.
- 이 목록에 있는 skill은 sync 대상에서 제외한다.
- 제외 의미는 아래와 같다.
  - source command가 있어도 자동 생성/갱신/덮어쓰기를 하지 않는다.
  - 전체 inventory 비교 시 누락으로 집계하지 않는다.
  - 최종 보고에서 `Codex 전용 예외`로 별도 보고한다.

| target skill | source command | 처리 방식 |
|--------------|----------------|----------|
| `orchestration` | `/orchestration` | Codex 전용 운영 스킬로 유지. Claude command 기준 자동 동기화 금지 |
| `harness` | `(none)` | Codex 전용 harness 관리 스킬. Claude source 없이 독립 유지 |

## 예외 규칙

- `claude/commands/**/_common.md` 같은 공용 헬퍼 파일은 leaf skill 매핑 대상이 아니다.
- `Codex 전용 예외 스킬 목록`에 있는 항목은 source command가 있어도 sync 대상에서 제외한다.
- 이름 충돌이 있는 경우, source command의 의미를 우선 보존한다.
  - 예: `/config:sync`는 `config-sync`로 유지
  - 매핑 작업용 스킬은 `skill-sync`를 사용
- 이미 target skill이 있어도 source command 의미와 다르면 덮어쓰지 말고 충돌을 먼저 정리한다.

## 이름 매핑 규칙

- Claude command: `/git:pr`
- Codex skill: `git-pr`

규칙:

1. command 그룹과 명령 이름을 `:` 기준으로 읽는다.
2. Codex skill 이름은 `group-name` 형식의 kebab-case로 만든다.
3. 콜론(`:`)은 쓰지 않는다.
4. 소문자, 숫자, 하이픈만 사용한다.

## 입력 해석 규칙

### source command에서 가져올 것

- frontmatter의 `description`
- `파라미터`
- `사전 체크`
- `작업`
- `주의사항`

### Codex skill로 옮길 때 바꿀 것

- Claude의 `/group:name` 호출 UX -> Codex의 `$group-name` 또는 skill 목록에서 선택
- `AskUserQuestion` -> 필요할 때 짧은 직접 질문
- `Task`/subagent 의존 -> Codex에서 실제로 허용된 경우만 사용, 아니면 메인 에이전트가 직접 수행
- `allowed-tools` -> Codex 스킬 본문에서는 “권장 도구/명령” 수준으로 번역

## 전수 동기화 절차

1. `Codex 전용 예외 스킬 목록`을 먼저 확인한다.
2. `claude/commands/**/*.md`를 전부 수집한다.
3. `_common.md` 같은 helper 파일을 제외한 source command inventory를 만든다.
4. 각 source command를 `group-name` 규칙으로 target skill 이름에 매핑한다.
5. 예외 스킬 목록과 대조해서 sync 제외 항목을 먼저 확정한다.
6. 이름 충돌, 예약 이름, 기존 special-case를 판정한다.
7. 누락된 target skill은 생성하고, 기존 target skill은 source 의미와 다르면 갱신한다.
8. 마지막에 source inventory와 target inventory를 다시 비교한다.
9. target skill의 frontmatter가 유효한지, 최소한 `name`과 `description`이 정상 파싱 가능한지 검증한다.
10. 파싱 실패 skill이 있으면 inventory상 파일이 있어도 누락으로 다시 집계한다.
11. 아래 항목을 반드시 보고한다.
   - 총 source command 수
   - 생성한 skill 수
   - 갱신한 skill 수
   - 예외 처리한 항목
   - 남은 누락 수

## 완료 조건

- helper 예외와 `Codex 전용 예외 스킬 목록`을 제외한 모든 source command에 대응 skill이 있어야 한다.
- 대응 skill은 Codex가 읽을 수 있는 정상 frontmatter를 가져야 한다.
- 남은 누락 수가 `0`이 아니면 완료로 보고하면 안 된다.
- 특정 카테고리만 처리했으면, 그건 "부분 작업"이라고 명시해야 한다.

## 변환 절차

1. `Codex 전용 예외 스킬 목록`을 먼저 확인해 현재 대상이 제외 항목인지 판정한다.
2. source command 파일을 끝까지 읽고 목적과 안전 규칙을 분리한다.
3. source inventory 기준으로 현재 작업 범위가 전체인지 부분인지 먼저 선언한다.
4. command를 leaf skill 하나로 만들지, umbrella + leaf 구조로 나눌지 결정한다.
5. Codex skill 이름을 정한다.
6. `SKILL.md` frontmatter를 작성한다.
7. 본문은 아래 구조를 기본으로 쓴다.

### 권장 본문 구조

```md
# 제목

## 언제 사용하나
- ...

## source mapping
- Claude command: `/git:pr`

## 기본 규칙
- ...

## 실행 절차
1. ...
2. ...

## 사용자에게 물어봐야 하는 경우
- ...

## 하지 말아야 할 것
- ...
```

## Git 계열 변환 규칙

- `git-convention`이 있으면 커밋 메시지/브랜치 규칙은 그 스킬을 따른다.
- `git-workflow`가 있으면 범용 안전 규칙은 그 스킬을 따른다.
- leaf skill은 “한 가지 행동”에 집중한다.
  - `git-save`: staging + commit
  - `git-push`: push
  - `git-pr`: PR 생성
  - `git-switch`: 브랜치 생성/전환
  - `git-sync`: rebase 동기화
  - `git-cleanup`: 머지된 브랜치 정리

## 품질 기준

- source command의 의도를 유지한다.
- Codex에서 지원되지 않는 기능을 있는 것처럼 쓰지 않는다.
- destructive 명령은 명시 요청 없이는 금지 규칙을 유지한다.
- 스킬 설명만 보고도 언제 써야 하는지 분명해야 한다.
- command 문서를 그대로 복붙하지 말고 Codex 실행 모델에 맞게 번역한다.
- Git만 만들고 Azure를 빠뜨리는 식의 부분 누락이 없도록 전수 검사 결과를 기준으로 완료를 선언한다.
- YAML frontmatter 문법이 깨져서 스킬 목록에 노출되지 않는 상태를 허용하지 않는다.
- Codex 전용으로 유지하기로 한 예외 skill은 Claude source 기준으로 되돌리거나 자동 덮어쓰지 않는다.

## 결과물 위치

- source: `ai-agent-config/claude/commands/<group>/<name>.md`
- target: `ai-agent-config/codex/skills/<group-name>/SKILL.md`
