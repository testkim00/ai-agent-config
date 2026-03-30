---
name: shared-push
description: 공유 모듈 변경사항을 원격 저장소에 푸시 Claude의 `/shared:push` 명령을 Codex에서 skill로 사용할 때 대응 매핑으로 사용한다.
---

# Shared Push

## 언제 사용하나

- 공유 모듈 변경사항을 원격 저장소에 푸시
- Claude의 `/shared:push`를 Codex에서 같은 의도로 수행해야 할 때

## source mapping

- Claude command: `/shared:push`
- Source file: `claude/commands/shared/push.md`

## 기본 규칙

- source command의 의도를 유지한다.
- Claude 전용 구문인 `allowed-tools`, `Task`, `AskUserQuestion`은 Codex 실행 환경에 맞게 해석한다.
- 사용자가 같은 동작을 요청하면 아래 source workflow를 기준으로 수행한다.

## source workflow


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

## Phase 1: 버전 확인

1. `src/_shared/_version.json` 읽기
2. `localModified: true`인 모듈 확인
3. 각 모듈별 로컬 변경사항 확인: `git diff --stat HEAD -- src/_shared/{모듈}`
4. 상태 테이블 표시:

| 모듈 | 현재 버전 | 로컬 수정 | 상태 |
|------|----------|----------|------|
| ui-shell | (커밋 앞 7자리) | ✅/❌ | 푸시 필요 / 변경 없음 |
| components | ... | ... | ... |
| core | ... | ... | ... |

5. 푸시할 모듈이 없으면 "푸시할 변경사항이 없습니다" 표시 후 종료

## Phase 2: 사전 확인

1. 변경사항 상세 표시
2. 커밋 안 됐으면 먼저 커밋 요청
3. "공유 모듈을 원격에 푸시하시겠습니까? 다른 프로젝트에도 영향을 미칩니다." 확인
4. 사용자 승인 후 진행

## Phase 3: Subtree Push

```bash
# 모듈별 원격 저장소
ui-shell:   https://github.com/testkim00/ui-shell.git
components: https://github.com/testkim00/ui-components.git
core:       https://github.com/testkim00/core-lib.git

# 푸시 명령 (localModified: true인 모듈만)
git subtree push --prefix=src/_shared/{모듈} {원격URL} main
```

## Phase 4: 버전 파일 업데이트

1. push 완료 후 원격 커밋 조회: `git ls-remote {원격URL} main`
2. `src/_shared/_version.json` 업데이트:
   - `lastSync`: 현재 시간 (ISO 8601 형식)
   - 각 모듈의 `commit`: 새로운 원격 커밋 해시
   - 각 모듈의 `localModified`: false

3. 버전 파일 변경사항 커밋:
```bash
git add src/_shared/_version.json
git commit -m "chore: 공유 모듈 버전 정보 업데이트 (push 완료)"
```

## Phase 5: 결과 안내

- 푸시 성공/실패 여부 표시
- 푸시된 모듈 목록
- 새 버전 정보 표시
