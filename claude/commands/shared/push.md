---
description: 공유 모듈 변경사항을 원격 저장소에 푸시
allowed-tools: Bash(git:*)
---

# 공유 모듈 푸시

현재 프로젝트의 _shared 모듈 변경사항을 원격 저장소에 푸시합니다.

## 사용법
- `/shared:push` - 변경된 모듈 모두 푸시
- `/shared:push ui-shell` - ui-shell만 푸시
- `/shared:push components` - components만 푸시
- `/shared:push core` - core만 푸시

## 인자
$ARGUMENTS

## 주의사항
- 공유 모듈을 수정한 경우에만 사용
- 다른 프로젝트에도 영향을 미치므로 신중하게 사용

---

# 처리 흐름

## Phase 1: 사전 확인

1. 변경사항 표시
2. 커밋 안 됐으면 먼저 커밋 요청
3. "공유 모듈을 원격에 푸시하시겠습니까? 다른 프로젝트에도 영향을 미칩니다." 확인
4. 사용자 승인 후 진행

## Phase 2: Subtree Push

```bash
# 모듈별 원격 저장소
ui-shell:   https://github.com/testkim00/ui-shell.git
components: https://github.com/testkim00/ui-components.git
core:       https://github.com/testkim00/core-lib.git

# 푸시 명령
git subtree push --prefix=src/_shared/{모듈} {원격URL} main
```

**all인 경우:**
```bash
git subtree push --prefix=src/_shared/ui-shell https://github.com/testkim00/ui-shell.git main
git subtree push --prefix=src/_shared/components https://github.com/testkim00/ui-components.git main
git subtree push --prefix=src/_shared/core https://github.com/testkim00/core-lib.git main
```

## Phase 3: 결과 안내

- 푸시 성공/실패 여부 표시
- 푸시된 모듈 목록
