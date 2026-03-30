---
name: config-push
description: AI 에이전트 설정 변경사항 원격에 푸시 Claude의 `/config:push` 명령을 Codex에서 skill로 사용할 때 대응 매핑으로 사용한다.
---

# Config Push

## 언제 사용하나

- AI 에이전트 설정 변경사항 원격에 푸시
- Claude의 `/config:push`를 Codex에서 같은 의도로 수행해야 할 때

## source mapping

- Claude command: `/config:push`
- Source file: `claude/commands/config/push.md`

## 기본 규칙

- source command의 의도를 유지한다.
- Claude 전용 구문인 `allowed-tools`, `Task`, `AskUserQuestion`은 Codex 실행 환경에 맞게 해석한다.
- 사용자가 같은 동작을 요청하면 아래 source workflow를 기준으로 수행한다.

## source workflow


# Config Push

로컬 설정 변경사항을 원격 저장소에 푸시합니다.

## 처리 흐름

1. 변경사항 확인
   ```bash
   cd ~/.ai-agent-config && git status --short
   ```

2. 변경 없으면 종료

3. 커밋 메시지 생성
   - 변경된 파일 기반으로 자동 생성
   - 형식: `config: {변경 요약}`

4. 커밋 및 푸시
   ```bash
   git add -A && git commit -m "{메시지}" && git push
   ```

## 결과 표시

- 푸시된 파일 목록
- 성공/실패 여부

## 참조

- 동기화 구조: `~/.claude/skills/sync-config/skill.md`
