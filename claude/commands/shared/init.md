---
description: 새 프로젝트에 공유 모듈(ui-shell, components, core) 추가 및 초기화
allowed-tools: Bash(git:*), Bash(npm:*), Bash(bash:*)
---

# 공유 모듈 초기화

새 프로젝트에 공유 모듈을 추가하고 초기화합니다.

## 사용법
- `/shared:init` - 3개 모듈 모두 추가
- `/shared:init ui-shell` - ui-shell만 추가
- `/shared:init components` - components만 추가
- `/shared:init core` - core만 추가

## 인자
$ARGUMENTS

## 사전 조건
- git 저장소 필요 (없으면 자동으로 `git init` 및 초기 커밋 생성)

---

# 처리 흐름

## Phase 1: 사전 확인

1. 현재 프로젝트 상태 표시
2. git 저장소 존재 확인 (없으면 생성)
3. "공유 모듈을 이 프로젝트에 추가하시겠습니까?" 확인
4. 사용자 승인 후 진행

## Phase 2: Subtree Add

```bash
# 모듈별 원격 저장소
ui-shell:   https://github.com/testkim00/ui-shell.git
components: https://github.com/testkim00/ui-components.git
core:       https://github.com/testkim00/core-lib.git

# 추가 명령
git subtree add --prefix=src/_shared/{모듈} {원격URL} main --squash
```

**all인 경우:**
```bash
git subtree add --prefix=src/_shared/ui-shell https://github.com/testkim00/ui-shell.git main --squash
git subtree add --prefix=src/_shared/components https://github.com/testkim00/ui-components.git main --squash
git subtree add --prefix=src/_shared/core https://github.com/testkim00/core-lib.git main --squash
```

## Phase 3: 초기화 (ui-shell 포함 시)

```bash
# 초기화 스크립트 실행
bash src/_shared/ui-shell/init-project.sh

# 의존성 설치
npm install
```

## Phase 4: 완료 안내

다음 단계 안내:
- package.json에서 name, description 수정
- quasar.config.js에서 API URL 수정
- npm run dev로 개발 서버 실행
