---
name: project-new
description: Claude command `/project:new` 대응 스킬. Claude의 `/project:new` 명령을 Codex에서 skill로 사용할 때 대응 매핑으로 사용한다.
---

# Project New

## 언제 사용하나

- Claude command `/project:new` 대응 스킬.
- Claude의 `/project:new`를 Codex에서 같은 의도로 수행해야 할 때

## source mapping

- Claude command: `/project:new`
- Source file: `claude/commands/project/new.md`

## 기본 규칙

- source command의 의도를 유지한다.
- Claude 전용 구문인 `allowed-tools`, `Task`, `AskUserQuestion`은 Codex 실행 환경에 맞게 해석한다.
- 사용자가 같은 동작을 요청하면 아래 source workflow를 기준으로 수행한다.

## source workflow

# Project New

새 프로젝트를 boilerplate 템플릿에서 생성합니다.

## 사용법

```
/project:new                    # 템플릿 선택 후 생성
/project:new erp-starter        # ERP 클라이언트 템플릿 (Vue3)
/project:new api-boilerplate    # API 서버 템플릿 (.NET 10)
/project:new <url>              # 커스텀 URL에서 생성
```

## 처리 흐름

```
┌─────────────────────────────────────────────────────────────────────┐
│ 1단계: 템플릿 선택                                                   │
│        ├ 인자가 없으면 → boilerplates.json에서 목록 표시             │
│        ├ 인자가 있으면 → 해당 템플릿 또는 URL 사용                    │
│        └ 프로젝트 이름 입력 받기                                     │
├─────────────────────────────────────────────────────────────────────┤
│ 2단계: 프로젝트 생성                                                 │
│        ├ 2-1. 템플릿 저장소 clone                                    │
│        ├ 2-2. .git 폴더 제거 (새 저장소로 시작)                       │
│        ├ 2-3. 프로젝트 파일 수정 (템플릿 타입에 따라)                  │
│        └ 2-4. 의존성 설치                                           │
├─────────────────────────────────────────────────────────────────────┤
│ 3단계: Shared 모듈 연결 (src/_shared 존재 시)                        │
│        ├ 3-1. git init (새 저장소 초기화)                            │
│        ├ 3-2. 초기 커밋 생성                                         │
│        ├ 3-3. src/_shared 폴더 삭제                                  │
│        ├ 3-4. subtree add로 각 모듈 연결                             │
│        └ (src/_shared 없으면 이 단계 건너뜀)                         │
├─────────────────────────────────────────────────────────────────────┤
│ 4단계: 초기화 완료                                                   │
│        ├ 4-1. 프로젝트 정보 표시                                     │
│        ├ 4-2. 다음 단계 안내                                         │
│        └ 4-3. 개발 서버 실행 여부 확인                                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 단계별 상세

### 1단계: 템플릿 선택

**인자가 없는 경우:**

`~/.claude/config/boilerplates.json`에서 목록을 읽어 선택지 표시:

```
"어떤 템플릿을 사용할까요?"
  ○ erp-starter - ERP 클라이언트 템플릿 (Quasar + Vue3)
  ○ api-boilerplate - API 서버 템플릿 (.NET 10)
  ○ Other (직접 입력)
```

**인자가 있는 경우:**

- `erp-starter`, `api-boilerplate` 등 → boilerplates.json에서 URL 조회
- `https://...` → 직접 URL 사용

**프로젝트 이름 입력:**

```
"프로젝트 이름을 입력하세요 (폴더명):"
→ MyNewProject
```

---

### 2단계: 프로젝트 생성

**공통:**

```bash
# 1. Clone
git clone {repo_url} {프로젝트명}

# 2. .git 제거 (새 저장소로 시작)
cd {프로젝트명}
rm -rf .git
```

**Vue/Quasar 프로젝트 (erp-starter):**

```bash
# 3. package.json 수정
# name, productName 등을 프로젝트명으로 변경

# 4. npm install
npm install
```

**.NET 프로젝트 (api-boilerplate):**

```bash
# 3. .csproj, .sln 파일명 및 내용 수정
mv *.csproj {프로젝트명}.csproj
mv *.sln {프로젝트명}.sln
# .sln 파일 내 프로젝트 참조 수정

# 4. dotnet restore
dotnet restore
```

---

### 3단계: Shared 모듈 연결 (NEW!)

**src/_shared 폴더가 존재하는 경우에만 실행:**

```bash
# 1. src/_shared 존재 확인
if [ -d "src/_shared" ]; then

  # 2. git 초기화 및 초기 커밋
  git init
  git add .
  git commit -m "초기 커밋: 프로젝트 템플릿 생성"

  # 3. 기존 _shared 폴더 삭제
  rm -rf src/_shared
  git add -A
  git commit -m "chore: _shared 폴더 제거 (subtree 연결 준비)"

  # 4. subtree로 각 모듈 연결
  git subtree add --prefix=src/_shared/ui-shell https://github.com/testkim00/ui-shell.git main --squash
  git subtree add --prefix=src/_shared/components https://github.com/testkim00/ui-components.git main --squash
  git subtree add --prefix=src/_shared/core https://github.com/testkim00/core-lib.git main --squash

fi
```

**src/_shared 폴더가 없으면:**
- 이 단계 건너뜀
- 일반 프로젝트로 진행

---

### 4단계: 초기화 완료

**다음 단계 안내 (Vue/Quasar + Shared 연결됨):**

```
✅ 프로젝트 생성 완료!

📦 Shared 모듈 연결됨:
  - ui-shell (subtree)
  - components (subtree)
  - core (subtree)

다음 단계:
1. cd {프로젝트명}
2. quasar dev        # 개발 서버 시작

Shared 모듈 관리:
- /shared:pull       # 최신 버전 가져오기
- /shared:push       # 변경사항 푸시

Git 원격 저장소 연결:
- git remote add origin <your-repo-url>
- git push -u origin main
```

**다음 단계 안내 (.NET):**

```
✅ 프로젝트 생성 완료!

다음 단계:
1. cd {프로젝트명}
2. dotnet run        # 개발 서버 시작
3. dotnet build      # 빌드

Git 초기화:
- git init
- git remote add origin <your-repo-url>
```

---

## 설정 파일

### ~/.claude/config/boilerplates.json

```json
{
  "erp-starter": {
    "repo": "https://github.com/testkim00/erp-starter",
    "desc": "ERP 클라이언트 템플릿 (Quasar + Vue3)",
    "tags": ["quasar", "vue3", "erp", "pinia"],
    "hasShared": true
  },
  "api-boilerplate": {
    "repo": "https://github.com/testkim00/api-boilerplate",
    "desc": "API 서버 템플릿 (.NET 10)",
    "tags": ["dotnet", "net10", "api", "efcore"],
    "hasShared": false
  }
}
```

---

## 예시

### erp-starter 템플릿 (Shared 연결 포함)

```
/project:new erp-starter

→ "프로젝트 이름을 입력하세요:"
  MyErpClient

→ [실행 중...]
  ✓ 템플릿 clone 완료
  ✓ .git 제거
  ✓ package.json 수정
  ✓ npm install 완료
  ✓ git init
  ✓ 초기 커밋 생성
  ✓ _shared 폴더 제거
  ✓ ui-shell subtree 연결
  ✓ components subtree 연결
  ✓ core subtree 연결

→ ✅ 프로젝트 생성 완료!

  📦 Shared 모듈 연결됨:
    - ui-shell
    - components
    - core

  다음 단계:
  1. cd MyErpClient
  2. quasar dev

  Shared 모듈 관리:
  - /shared:pull  # 최신 버전 가져오기
  - /shared:push  # 변경사항 푸시

→ "지금 quasar dev를 실행할까요?"
  ● Yes
```

### api-boilerplate 템플릿 (Shared 없음)

```
/project:new api-boilerplate

→ "프로젝트 이름을 입력하세요:"
  MyApiServer

→ [실행 중...]
  ✓ 템플릿 clone 완료
  ✓ .git 제거
  ✓ .csproj/.sln 수정
  ✓ dotnet restore 완료

→ ✅ 프로젝트 생성 완료!

  다음 단계:
  1. cd MyApiServer
  2. dotnet run

→ "지금 dotnet run을 실행할까요?"
  ● No
```

---

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/shared:init` | 기존 프로젝트에 _shared 수동 추가 |
| `/shared:pull` | _shared 최신화 |
| `/shared:push` | _shared 변경 푸시 |
