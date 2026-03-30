---
name: shared-init
description: 새 프로젝트에 공유 모듈(ui-shell, components, core) 추가 및 초기화 Claude의 `/shared:init` 명령을 Codex에서 skill로 사용할 때 대응 매핑으로 사용한다.
---

# Shared Init

## 언제 사용하나

- 새 프로젝트에 공유 모듈(ui-shell, components, core) 추가 및 초기화
- Claude의 `/shared:init`를 Codex에서 같은 의도로 수행해야 할 때

## source mapping

- Claude command: `/shared:init`
- Source file: `claude/commands/shared/init.md`

## 기본 규칙

- source command의 의도를 유지한다.
- Claude 전용 구문인 `allowed-tools`, `Task`, `AskUserQuestion`은 Codex 실행 환경에 맞게 해석한다.
- 사용자가 같은 동작을 요청하면 아래 source workflow를 기준으로 수행한다.

## source workflow


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
3. 기존 `src/_shared/_version.json` 존재 여부 확인
4. "공유 모듈을 이 프로젝트에 추가하시겠습니까?" 확인
5. 사용자 승인 후 진행

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

## Phase 3: 버전 파일 생성

1. 각 모듈별 원격 커밋 조회: `git ls-remote {원격URL} main`
2. `src/_shared/_version.json` 생성:

```json
{
  "version": "1.0.0",
  "lastSync": "{현재시간 ISO 8601}",
  "modules": {
    "ui-shell": {
      "remote": "https://github.com/testkim00/ui-shell.git",
      "branch": "main",
      "commit": "{원격 커밋 해시}",
      "localModified": false
    },
    "components": {
      "remote": "https://github.com/testkim00/ui-components.git",
      "branch": "main",
      "commit": "{원격 커밋 해시}",
      "localModified": false
    },
    "core": {
      "remote": "https://github.com/testkim00/core-lib.git",
      "branch": "main",
      "commit": "{원격 커밋 해시}",
      "localModified": false
    }
  }
}
```

3. 버전 파일 커밋:
```bash
git add src/_shared/_version.json
git commit -m "chore: 공유 모듈 버전 파일 생성"
```

## Phase 4: 초기화 (ui-shell 포함 시)

```bash
# 초기화 스크립트 실행
bash src/_shared/ui-shell/init-project.sh

# 의존성 설치
npm install
```

## Phase 5: 완료 안내

버전 정보 표시:

| 모듈 | 버전 | 원격 저장소 |
|------|------|------------|
| ui-shell | (커밋 앞 7자리) | github.com/testkim00/ui-shell |
| components | (커밋 앞 7자리) | github.com/testkim00/ui-components |
| core | (커밋 앞 7자리) | github.com/testkim00/core-lib |

다음 단계 안내:
- package.json에서 name, description 수정
- quasar.config.js에서 API URL 수정
- npm run dev로 개발 서버 실행
