# Project New

새 프로젝트를 boilerplate 템플릿에서 생성합니다.

## 사용법

```
/project:new              # 템플릿 선택 후 생성
/project:new erp          # erp-starter 템플릿으로 생성
/project:new <url>        # 커스텀 URL에서 생성
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
│        ├ 2-3. package.json 프로젝트명 수정                           │
│        └ 2-4. npm install                                           │
├─────────────────────────────────────────────────────────────────────┤
│ 3단계: 초기화 완료                                                   │
│        ├ 3-1. _shared 버전 정보 표시                                 │
│        ├ 3-2. 다음 단계 안내                                         │
│        └ 3-3. quasar dev 실행 여부 확인                              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 단계별 상세

### 1단계: 템플릿 선택

**인자가 없는 경우:**

`~/.claude/config/boilerplates.json`에서 목록을 읽어 선택지 표시:

```
"어떤 템플릿을 사용할까요?"
  ○ erp - ERP 클라이언트 템플릿 (Quasar + Vue3)
  ○ admin - 관리자 포털 템플릿
  ○ Other (직접 입력)
```

**인자가 있는 경우:**

- `erp`, `admin` 등 → boilerplates.json에서 URL 조회
- `https://...` → 직접 URL 사용

**프로젝트 이름 입력:**

```
"프로젝트 이름을 입력하세요 (폴더명):"
→ my-erp-project
```

---

### 2단계: 프로젝트 생성

```bash
# 1. Clone
git clone https://github.com/testkim00/erp-starter.git {프로젝트명}

# 2. .git 제거 (새 저장소로 시작)
cd {프로젝트명}
rm -rf .git

# 3. package.json 수정
# name, productName 등을 프로젝트명으로 변경

# 4. npm install
npm install
```

---

### 3단계: 초기화 완료

**_shared 버전 정보 표시:**

`_shared-version.json` 파일 읽어서 표시:

```
■ _shared 모듈 버전
┌─────────────────────────────────────────────────────────────┐
│ ui-shell:   v1.0.0 (13e8582e)                               │
│ components: v1.0.0 (dcab6f15)                               │
│ core:       v1.0.0 (d3b0e6bd)                               │
└─────────────────────────────────────────────────────────────┘
```

**다음 단계 안내:**

```
✅ 프로젝트 생성 완료!

다음 단계:
1. cd {프로젝트명}
2. quasar dev        # 개발 서버 시작
3. quasar build      # 프로덕션 빌드

_shared 모듈 업데이트:
- /project:sync-shared  # 최신 버전으로 동기화

Git 초기화:
- git init
- git remote add origin <your-repo-url>
```

---

## 설정 파일

### ~/.claude/config/boilerplates.json

```json
{
  "erp": {
    "repo": "https://github.com/testkim00/erp-starter",
    "desc": "ERP 클라이언트 템플릿 (Quasar + Vue3)",
    "tags": ["quasar", "vue3", "erp"]
  },
  "admin": {
    "repo": "https://github.com/testkim00/admin-starter",
    "desc": "관리자 포털 템플릿",
    "tags": ["quasar", "vue3", "admin"]
  }
}
```

---

## 예시

```
/project:new

→ "어떤 템플릿을 사용할까요?"
  ● erp - ERP 클라이언트 템플릿 (Quasar + Vue3)

→ "프로젝트 이름을 입력하세요:"
  my-new-erp

→ [실행 중...]
  ✓ 템플릿 clone 완료
  ✓ .git 제거
  ✓ package.json 수정
  ✓ npm install 완료

→ ✅ 프로젝트 생성 완료!

  ■ _shared 모듈 버전
  │ ui-shell:   v1.0.0 (13e8582e)
  │ components: v1.0.0 (dcab6f15)
  │ core:       v1.0.0 (d3b0e6bd)

  다음 단계:
  1. cd my-new-erp
  2. quasar dev

→ "지금 quasar dev를 실행할까요?"
  ● Yes
```

---

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/project:init-shared` | 기존 프로젝트에 _shared 추가 |
| `/project:sync-shared` | _shared 최신화 |
| `/project:push-shared` | _shared 변경 푸시 |
