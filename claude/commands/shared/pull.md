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

## Phase 1: 버전 확인

1. `src/_shared/_version.json` 읽기
2. 각 모듈별 원격 커밋 조회: `git ls-remote {원격URL} main`
3. 버전 비교 테이블 표시:

| 모듈 | 로컬 버전 | 원격 버전 | 상태 |
|------|----------|----------|------|
| ui-shell | (커밋 앞 7자리) | (커밋 앞 7자리) | ✅ 최신 / ⬇️ 업데이트 필요 |
| components | ... | ... | ... |
| core | ... | ... | ... |

4. `localModified: true`인 모듈은 ⚠️ 로컬 수정됨 표시
5. 업데이트 필요한 모듈이 없으면 "모든 모듈이 최신 상태입니다" 표시 후 종료

## Phase 2: 사전 확인

1. 커밋 안 된 변경사항 있으면 경고
2. "공유 모듈을 원격에서 가져오시겠습니까?" 확인
3. 사용자 승인 후 진행

## Phase 3: Subtree Pull

```bash
# 모듈별 원격 저장소
ui-shell:   https://github.com/testkim00/ui-shell.git
components: https://github.com/testkim00/ui-components.git
core:       https://github.com/testkim00/core-lib.git

# 풀 명령
git subtree pull --prefix=src/_shared/{모듈} {원격URL} main --squash
```

## Phase 4: 버전 파일 업데이트

1. pull 완료 후 `src/_shared/_version.json` 업데이트:
   - `lastSync`: 현재 시간 (ISO 8601 형식)
   - 각 모듈의 `commit`: 새로운 원격 커밋 해시
   - 각 모듈의 `localModified`: false

2. 버전 파일 변경사항 커밋:
```bash
git add src/_shared/_version.json
git commit -m "chore: 공유 모듈 버전 정보 업데이트"
```

## Phase 5: 결과 안내

- 동기화된 모듈 표시
- 업데이트된 파일 목록
- 새 버전 정보 표시
