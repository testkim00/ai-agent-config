---
description: 공유 모듈(ui-shell, components, core) 최신 버전으로 업데이트
allowed-tools: Bash(git:*)
---

# 공유 모듈 풀

원격 저장소의 최신 변경사항을 현재 프로젝트로 가져옵니다.

## 사용법
- `/shared:pull` - 3개 모듈 모두 동기화
- `/shared:pull ui-shell` - ui-shell만 동기화
- `/shared:pull components` - components만 동기화
- `/shared:pull core` - core만 동기화

## 인자
$ARGUMENTS

---

# 처리 흐름

## Phase 1: 사전 확인

1. 현재 상태 표시
2. 커밋 안 된 변경사항 있으면 경고
3. "공유 모듈을 원격에서 가져오시겠습니까?" 확인
4. 사용자 승인 후 진행

## Phase 2: Subtree Pull

```bash
# 모듈별 원격 저장소
ui-shell:   https://github.com/testkim00/ui-shell.git
components: https://github.com/testkim00/ui-components.git
core:       https://github.com/testkim00/core-lib.git

# 풀 명령
git subtree pull --prefix=src/_shared/{모듈} {원격URL} main --squash
```

**all인 경우:**
```bash
git subtree pull --prefix=src/_shared/ui-shell https://github.com/testkim00/ui-shell.git main --squash
git subtree pull --prefix=src/_shared/components https://github.com/testkim00/ui-components.git main --squash
git subtree pull --prefix=src/_shared/core https://github.com/testkim00/core-lib.git main --squash
```

## Phase 3: 결과 안내

- 동기화된 모듈 표시
- 업데이트된 파일 목록
- 변경된 파일 수
