---
description: AI 에이전트 설정 변경사항 원격에 푸시
allowed-tools: Bash(git:*)
---

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
