---
description: 새 프로젝트에 공유 모듈(ui-shell, components, core) 추가 및 초기화
allowed-tools: Bash(git:*), Bash(npm:*), Bash(bash:*)
---

# 공유 모듈 프로젝트 초기화

이 커맨드는 새 프로젝트에 공유 모듈을 추가하고 초기화합니다.

## 사용법
- `/project:init-shared` - 3개 모듈 모두 추가
- `/project:init-shared ui-shell` - ui-shell만 추가
- `/project:init-shared components` - components만 추가
- `/project:init-shared core` - core만 추가

## 인자
$ARGUMENTS

## 사전 조건
- git 저장소 필요 (없으면 자동으로 `git init` 및 초기 커밋 생성)

---

# 처리 흐름 (Subagent 활용)

> 모델 설정: `~/.claude/skills/subagent-convention/config.md` 참조

## 역할 분담

| 역할 | 담당 | 작업 |
|------|------|------|
| **판단** | Opus (메인) | 사용자 확인, 모듈 선택 |
| **실행** | Sonnet subagent | git subtree 명령, npm install |

## Phase 1: 판단 (Opus)

1. 현재 프로젝트 상태 표시
2. "공유 모듈을 이 프로젝트에 추가하시겠습니까?" 확인
3. 사용자 승인 후 진행

## Phase 2: 모듈 추가 (Sonnet Subagent)

```
Task(
    subagent_type="sonnet",
    model="sonnet",
    prompt="""
    공유 모듈 초기화 작업:

    추가할 모듈: {all/ui-shell/components/core}

    1. 현재 상태 확인
       - git status
       - src/_shared 폴더 존재 확인

    2. Subtree 추가
       all인 경우:
       - git subtree add --prefix=src/_shared/ui-shell https://github.com/testkim00/ui-shell.git main --squash
       - git subtree add --prefix=src/_shared/components https://github.com/testkim00/ui-components.git main --squash
       - git subtree add --prefix=src/_shared/core https://github.com/testkim00/core-lib.git main --squash

       개별 모듈인 경우 해당 명령만 실행

    3. 초기화 스크립트 (ui-shell 포함 시)
       - bash src/_shared/ui-shell/init-project.sh

    4. 의존성 설치
       - npm install

    5. 결과 반환
       - 추가된 모듈 목록
       - 성공/실패 여부
    """
)
```

## Phase 3: 완료 안내 (Opus)

- 다음 단계 안내:
  - package.json에서 name, description 수정
  - quasar.config.js에서 API URL 수정
  - npm run dev로 개발 서버 실행
