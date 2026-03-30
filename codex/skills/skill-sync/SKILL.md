---
name: skill-sync
description: ai-agent-config의 Claude commands를 Codex skills로 대응 매핑하고 동기화할 때 사용한다. `/git:pr` 같은 Claude 명령을 `git-pr` 같은 Codex skill로 옮기거나, command frontmatter와 워크플로우를 Codex 실행 규칙에 맞게 번역해야 할 때 사용한다.
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

## 변환 절차

1. source command 파일을 끝까지 읽고 목적과 안전 규칙을 분리한다.
2. command를 leaf skill 하나로 만들지, umbrella + leaf 구조로 나눌지 결정한다.
3. Codex skill 이름을 정한다.
4. `SKILL.md` frontmatter를 작성한다.
5. 본문은 아래 구조를 기본으로 쓴다.

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

## 결과물 위치

- source: `ai-agent-config/claude/commands/<group>/<name>.md`
- target: `ai-agent-config/codex/skills/<group-name>/SKILL.md`
