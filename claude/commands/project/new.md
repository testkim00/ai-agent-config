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
│        │      - Vue: package.json 수정 → npm install                │
│        │      - .NET: .csproj/.sln 수정 → dotnet restore            │
│        └ 2-4. 의존성 설치                                           │
├─────────────────────────────────────────────────────────────────────┤
│ 3단계: 초기화 완료                                                   │
│        ├ 3-1. 프로젝트 정보 표시                                     │
│        ├ 3-2. 다음 단계 안내                                         │
│        └ 3-3. 개발 서버 실행 여부 확인                                │
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

### 3단계: 초기화 완료

**다음 단계 안내 (Vue/Quasar):**

```
✅ 프로젝트 생성 완료!

다음 단계:
1. cd {프로젝트명}
2. quasar dev        # 개발 서버 시작
3. quasar build      # 프로덕션 빌드

Git 초기화:
- git init
- git remote add origin <your-repo-url>
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
    "tags": ["quasar", "vue3", "erp", "pinia"]
  },
  "api-boilerplate": {
    "repo": "https://github.com/testkim00/api-boilerplate",
    "desc": "API 서버 템플릿 (.NET 10)",
    "tags": ["dotnet", "net10", "api", "efcore"]
  }
}
```

---

## 예시

### erp-starter 템플릿

```
/project:new erp-starter

→ "프로젝트 이름을 입력하세요:"
  MyErpClient

→ [실행 중...]
  ✓ 템플릿 clone 완료
  ✓ .git 제거
  ✓ package.json 수정
  ✓ npm install 완료

→ ✅ 프로젝트 생성 완료!

  다음 단계:
  1. cd MyErpClient
  2. quasar dev

→ "지금 quasar dev를 실행할까요?"
  ● Yes
```

### api-boilerplate 템플릿

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
| `/project:init-shared` | 기존 프로젝트에 _shared 추가 |
| `/project:sync-shared` | _shared 최신화 |
| `/project:push-shared` | _shared 변경 푸시 |
