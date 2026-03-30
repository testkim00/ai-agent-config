---
name: project-structure
description: Claude command `/project:structure` 대응 스킬. Claude의 `/project:structure` 명령을 Codex에서 skill로 사용할 때 대응 매핑으로 사용한다.
---

# Project Structure

## 언제 사용하나

- Claude command `/project:structure` 대응 스킬.
- Claude의 `/project:structure`를 Codex에서 같은 의도로 수행해야 할 때

## source mapping

- Claude command: `/project:structure`
- Source file: `claude/commands/project/structure.md`

## 기본 규칙

- source command의 의도를 유지한다.
- Claude 전용 구문인 `allowed-tools`, `Task`, `AskUserQuestion`은 Codex 실행 환경에 맞게 해석한다.
- 사용자가 같은 동작을 요청하면 아래 source workflow를 기준으로 수행한다.

## source workflow

# Project Structure

프로젝트의 구조를 분석하여 AI가 활용할 수 있는 명세 문서(`PROJECT_STRUCTURE.md`)를 생성합니다.

## 사용법

```
/project:structure                              # 현재 프로젝트 분석
/project:structure /path/to/project             # 지정 경로 분석
/project:structure ERP서버                       # 별칭으로 분석 (projects.yaml 참조)
/project:structure --update                     # 기존 문서 갱신 (변경된 부분만)
/project:structure --depth 3                    # 디렉토리 트리 깊이 지정 (기본: 3)
/project:structure ERP서버 --update              # 별칭 + 옵션 조합
```

## 처리 흐름

```
┌─────────────────────────────────────────────────────────────────────┐
│ 1단계: 대상 결정 및 프로젝트 감지                                      │
│        ├ 인자 해석: 경로 / 별칭 / 없음(현재 디렉토리)                  │
│        ├ 별칭이면 → projects.yaml에서 경로 조회                       │
│        ├ 프로젝트 루트 확인 (.git, *.csproj, package.json 등)        │
│        ├ 기술 스택 감지 (언어, 프레임워크)                             │
│        └ 기존 PROJECT_STRUCTURE.md 존재 여부 확인                     │
├─────────────────────────────────────────────────────────────────────┤
│ 2단계: 구조 수집 (Setter)                                            │
│        ├ 2-1. 디렉토리 트리 수집 (불필요 디렉토리 제외)                │
│        ├ 2-2. 핵심 파일 식별 (엔트리포인트, 설정, 라우팅 등)           │
│        ├ 2-3. 의존성 분석 (패키지 매니저 파일)                         │
│        └ 2-4. 기술 스택별 추가 분석                                   │
├─────────────────────────────────────────────────────────────────────┤
│ 3단계: 패턴 분석                                                      │
│        ├ 3-1. 아키텍처 패턴 (레이어, 모듈, DI 등)                     │
│        ├ 3-2. 코딩 컨벤션 (네이밍, 파일 구조)                         │
│        ├ 3-3. 데이터 모델 요약 (DB 컨텍스트, 엔티티)                   │
│        ├ 3-4. API 엔드포인트 수집 (해당 시)                           │
│        ├ 3-5. 초기화/부트 체인 (부트 순서, 전역 등록 객체)            │
│        ├ 3-6. HTTP 통신 패턴 (인터셉터, 캐싱, 타임아웃)              │
│        ├ 3-7. 인증/권한 흐름 (토큰, 세션, 권한 체크)                  │
│        ├ 3-8. 에러 처리 체계 (커스텀 에러, 전역 핸들러)               │
│        ├ 3-9. 공통 컴포넌트 분류 (카테고리별 주요 컴포넌트)           │
│        └ 3-10. 새 모듈 추가 레시피 도출 (기존 모듈 패턴 기반)         │
├─────────────────────────────────────────────────────────────────────┤
│ 4단계: 문서 생성                                                      │
│        ├ 4-1. 출력 템플릿에 맞춰 문서 작성                             │
│        ├ 4-2. 프로젝트 루트에 PROJECT_STRUCTURE.md 생성                │
│        └ 4-3. 결과 요약 출력                                          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 단계별 상세

### 1단계: 대상 결정 및 프로젝트 감지

**인자 해석 (우선순위):**

| 인자 형태 | 해석 | 예시 |
|----------|------|------|
| 없음 | 현재 작업 디렉토리 | `/project:structure` |
| `/`로 시작 | 절대 경로 | `/project:structure /Users/.../WooriErp` |
| `./` 또는 `../`로 시작 | 상대 경로 | `/project:structure ./WooriErp` |
| 그 외 문자열 | 별칭 → `projects.yaml`에서 경로 조회 | `/project:structure ERP서버` |

**별칭 조회 흐름:**
1. `~/.claude/config/projects.yaml`에서 `aliases` 매칭
2. 매칭되면 해당 `path`를 대상 경로로 사용
3. 매칭 실패 시 → 경로로 시도 → 실패 시 에러

**프로젝트 루트 판별 기준 (우선순위):**

| 파일/폴더 | 프로젝트 타입 |
|-----------|-------------|
| `*.sln` / `*.csproj` | .NET |
| `package.json` | Node.js / Vue / React |
| `requirements.txt` / `pyproject.toml` / `setup.py` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml` / `build.gradle` | Java |
| `docker-compose.yml` (단독) | 멀티 서비스 |

**프레임워크 세부 감지:**

| 조건 | 프레임워크 |
|------|----------|
| `quasar.config` 존재 | Quasar (Vue3) |
| `nuxt.config` 존재 | Nuxt |
| `next.config` 존재 | Next.js |
| `vite.config` 존재 | Vite |
| `Program.cs` + `*.csproj` | ASP.NET |
| `manage.py` 존재 | Django |
| `app.py` / `main.py` + Flask import | Flask / FastAPI |

---

### 2단계: 구조 수집

**디렉토리 트리 수집 규칙:**

제외 대상:
```
node_modules, bin, obj, .git, dist, build, __pycache__,
.vs, .vscode, .idea, coverage, .next, .nuxt, .output,
*.lock, *.log
```

**핵심 파일 식별 기준:**

| 카테고리 | 대상 파일 |
|---------|----------|
| 엔트리포인트 | `Program.cs`, `main.ts`, `main.js`, `app.py`, `index.ts`, `App.vue` |
| 설정 | `appsettings*.json`, `vite.config.*`, `quasar.config.*`, `.env*` |
| 라우팅 | `router/`, `Controllers/`, `routes/` |
| 상태관리 | `stores/`, `store/` |
| 데이터 | `Models/`, `Entities/`, `migrations/`, `DbContext` |
| 미들웨어/확장 | `Extensions/`, `Middlewares/`, `plugins/` |
| 부트/초기화 | `boot/`, `plugins/`, DI 등록 파일 |
| HTTP 클라이언트 | `HttpService*`, `http/`, `api/client*`, `axios*` |
| 인증 | `auth/`, `AuthService*`, `authStore*` |
| 에러 처리 | `ErrorTypes*`, `Tripwire*`, `errorHandler*` |
| 공통 컴포넌트 | `components/`, `_shared/`, `common/` |
| 엔드포인트 정의 | `EndPoints*`, `endpoints*`, `api.ts` |
| 테스트 | `tests/`, `__tests__/`, `*.Tests/` |

**의존성 분석:**

- `package.json` → dependencies, devDependencies 주요 항목
- `*.csproj` → PackageReference 목록
- `requirements.txt` / `pyproject.toml` → 패키지 목록
- 주요 라이브러리만 추출 (유틸/보조 라이브러리 생략)

---

### 3단계: 패턴 분석

**아키텍처 패턴 감지:**

| 패턴 | 감지 기준 |
|------|----------|
| Layered (N-tier) | Controllers → Services → Repositories 구조 |
| Clean Architecture | Domain/, Application/, Infrastructure/ 분리 |
| Feature-based | Features/ 또는 Modules/ 단위 구조 |
| MVC | Models/, Views/, Controllers/ 존재 |
| Component-based | components/, pages/, layouts/ 존재 |
| Monorepo | packages/, apps/ 존재 |

**코딩 컨벤션 감지:**
- 파일/폴더 네이밍 (PascalCase, camelCase, kebab-case)
- 클래스/함수 네이밍 패턴
- 들여쓰기 스타일 (`.editorconfig` 참조)

**초기화/부트 체인 분석:**
- 부트 파일 로드 순서 (quasar boot, next.config, main.ts 등)
- `globalThis`/`window`에 등록되는 전역 객체 추적
- 전역 유틸리티 함수 (notify, loader 등) 목록화

**HTTP 통신 패턴 분석:**
- HTTP 클라이언트 파일 위치 및 래퍼 구조
- 요청 인터셉터 (인증 토큰 주입, 에러 변환)
- 응답 캐싱 전략 (TTL, LRU 등)
- 타임아웃 프로파일
- 로그 자동 기록 여부 (POST/PATCH/DELETE 시)

**인증/권한 흐름 분석:**
- 인증 방식 (SSO, JWT, Cookie, OAuth 등)
- 토큰 저장/갱신 위치 (Cookie, localStorage, SessionStorage)
- 권한 체크 API (can(), hasRole() 등)
- 세션 관리 방식

**에러 처리 체계 분석:**
- 커스텀 에러 클래스 (ErrorTypes 등)
- 전역 에러 핸들러 (Vue errorHandler, window.onerror 등)
- 에러 콜백 패턴 (Tripwire 등)
- 재시도 가능 에러 구분

**공통 컴포넌트 분류:**
- 카테고리별 주요 컴포넌트 역할 (grids, controls, dialog, buttons 등)
- Base 컴포넌트 패턴 (상속/합성 구조)

**새 모듈 추가 레시피 도출:**
- 기존 모듈 1~2개를 대표로 분석
- 생성해야 할 파일 목록과 순서 (의존성 순)
- 각 파일의 네이밍 패턴
- 코드 수정 없이 필요한 설정 (메뉴 등록, 라우트 자동 등록 등)

---

### 4단계: 문서 생성

**출력 파일:** `{프로젝트 루트}/PROJECT_STRUCTURE.md`

**출력 형식:** `~/.claude/skills/project-structure/skill.md`의 템플릿 참조

**--update 옵션 시:**
- 기존 `PROJECT_STRUCTURE.md` 읽기
- 변경된 섹션만 갱신 (수동 작성 섹션 보존)
- `<!-- manual -->` 주석이 있는 섹션은 건드리지 않음

---

## 출력 예시

```
🔍 프로젝트 분석 중...

  프로젝트: WooriErp
  타입: ASP.NET 10 Web API
  프레임워크: ASP.NET Core

📂 구조 수집 완료
  - 디렉토리: 24개
  - 핵심 파일: 12개
  - 의존성: 18개

🏗️ 패턴 분석 완료
  - 아키텍처: Layered (Controllers → Services)
  - 네이밍: PascalCase
  - DB 컨텍스트: 3개

✅ PROJECT_STRUCTURE.md 생성 완료!

  파일 위치: /Users/.../WooriErp/PROJECT_STRUCTURE.md
  문서 크기: 약 150줄

  💡 이 문서는 CLAUDE.md에서 참조하면 AI가 자동으로 활용합니다.
```

---

## 주의사항

- **민감 정보 제외**: 연결 문자열, API 키, 시크릿은 문서에 포함하지 않음
- **적정 크기 유지**: 문서가 300줄을 초과하면 요약 수준 조정
- **수동 섹션 보존**: `<!-- manual -->` 주석 블록은 --update 시 건드리지 않음
- **.gitignore 확인**: 필요 시 `.gitignore`에 추가 여부 확인

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/project:new` | 새 프로젝트 생성 |
| `/tidy:meta` | 메타 파일 정리 |
| `/orchestration` | 복잡한 작업 체계적 수행 |
