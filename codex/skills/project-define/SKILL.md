---
name: project-define
description: Claude command `/project:define` 대응 스킬. Claude의 `/project:define` 명령을 Codex에서 skill로 사용할 때 대응 매핑으로 사용한다.
---

# Project Define

## 언제 사용하나

- Claude command `/project:define` 대응 스킬.
- Claude의 `/project:define`를 Codex에서 같은 의도로 수행해야 할 때

## source mapping

- Claude command: `/project:define`
- Source file: `claude/commands/project/define.md`

## 기본 규칙

- source command의 의도를 유지한다.
- Claude 전용 구문인 `allowed-tools`, `Task`, `AskUserQuestion`은 Codex 실행 환경에 맞게 해석한다.
- 사용자가 같은 동작을 요청하면 아래 source workflow를 기준으로 수행한다.

## source workflow

# Project Define

프로젝트를 전역 레지스트리에 등록합니다. 등록된 프로젝트는 별칭으로 참조할 수 있습니다.

## 사용법

```
/project:define <별칭> <설명>
/project:define                        # 대화형으로 등록
/project:define --list                 # 등록된 프로젝트 목록
/project:define --remove <별칭>        # 등록 해제
```

## 예시

```
/project:define ERP서버 "우리관리 ERP 백엔드 API"
/project:define ERP클라이언트 "우리관리 ERP 프론트엔드"
/project:define 데이터포털 "데이터 분석 포털"
```

## 처리 흐름

```
┌─────────────────────────────────────────────────────────────────────┐
│ 1단계: 프로젝트 정보 수집                                            │
│        ├ 현재 디렉토리에서 프로젝트 루트 확인                         │
│        ├ 인자에서 별칭, 설명 추출                                     │
│        └ 인자 없으면 대화형으로 입력 받기                              │
├─────────────────────────────────────────────────────────────────────┤
│ 2단계: 자동 감지                                                     │
│        ├ 프로젝트명: 폴더명 또는 sln/package.json의 name             │
│        ├ 기술 스택: 프로젝트 파일로 자동 판별                         │
│        ├ 타입: 자동 추론 (server/client/fullstack/library)           │
│        └ 기존 등록 여부 확인 (같은 경로면 갱신)                       │
├─────────────────────────────────────────────────────────────────────┤
│ 3단계: 레지스트리 등록                                                │
│        ├ ~/.claude/config/projects.yaml 갱신                         │
│        └ 결과 출력                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 단계별 상세

### 1단계: 프로젝트 정보 수집

**인자가 있는 경우:**

```
/project:define ERP서버 "우리관리 ERP 백엔드 API"
                ──────  ──────────────────────────
                별칭     설명
```

- 별칭: 공백 없는 첫 번째 인자 (여러 별칭은 쉼표 구분)
- 설명: 나머지 텍스트

**여러 별칭 등록:**

```
/project:define ERP서버,ERP백엔드,우리ERP "우리관리 ERP 백엔드 API"
```

**인자가 없는 경우 (대화형):**

```
"프로젝트 별칭을 입력하세요 (여러 개는 쉼표 구분):"
→ ERP서버, ERP백엔드

"프로젝트 설명을 입력하세요:"
→ 우리관리 ERP 백엔드 API
```

---

### 2단계: 자동 감지

**프로젝트명:**
- `.sln` → 솔루션명
- `package.json` → name 필드
- `pyproject.toml` → project.name
- 그 외 → 폴더명

**기술 스택 감지:**

| 감지 파일 | 스택 |
|----------|------|
| `*.csproj` + `Program.cs` | .NET |
| `package.json` + `quasar.config.*` | Vue3 + Quasar |
| `package.json` + `vite.config.*` | Vue3 / React + Vite |
| `package.json` + `nuxt.config.*` | Nuxt |
| `package.json` + `next.config.*` | Next.js |
| `requirements.txt` / `pyproject.toml` | Python |
| `go.mod` | Go |

**타입 자동 추론:**

| 조건 | 타입 |
|------|------|
| Controllers/ 또는 API 엔드포인트 존재 | `server` |
| src/pages/ 또는 src/views/ 존재 | `client` |
| 둘 다 존재 | `fullstack` |
| src/lib/ 또는 패키지로 배포 구조 | `library` |

> 자동 추론 결과가 부정확하면 사용자에게 확인

---

### 3단계: 레지스트리 등록

**파일:** `~/.claude/config/projects.yaml`

**형식:**

```yaml
projects:
  - name: WooriErp              # 프로젝트명 (자동 감지)
    path: /Users/.../WooriErp   # 프로젝트 경로
    type: server                # server | client | fullstack | library
    stack: ".NET 10"            # 기술 스택
    aliases:                    # 사용자가 부를 수 있는 이름들
      - "ERP서버"
      - "ERP백엔드"
      - "우리ERP"
    description: "우리관리 ERP 백엔드 API"
```

**같은 경로의 프로젝트가 이미 등록된 경우:**
- 별칭 추가 (기존 별칭 유지)
- 설명 갱신
- 스택/타입은 재감지

**별칭 충돌 시:**
- 다른 프로젝트에 같은 별칭이 있으면 경고 후 확인

---

## --list 옵션

```
/project:define --list
```

출력:

```
📋 등록된 프로젝트 (4개)

  WooriErp [server] .NET 10
  경로: /Users/.../WooriErp
  별칭: ERP서버, ERP백엔드, 우리ERP
  설명: 우리관리 ERP 백엔드 API

  WooriErpClient [client] Vue3 + Quasar
  경로: /Users/.../WooriErpClient
  별칭: ERP클라이언트, ERP프론트
  설명: 우리관리 ERP 프론트엔드

  DataPortal [fullstack] Python
  경로: /Users/.../DataPortal
  별칭: 데이터포털
  설명: 데이터 분석 포털

  WooriApi [server] .NET 10
  경로: /Users/.../WooriApi
  별칭: API서버, 연동API
  설명: 타시스템 연동용 API 서버
```

---

## --remove 옵션

```
/project:define --remove ERP서버
```

- 해당 별칭이 포함된 프로젝트를 레지스트리에서 제거
- 확인 후 실행

---

## AI 활용 방식

레지스트리가 등록되면 AI는 다음과 같이 활용합니다:

```
사용자: "ERP서버에서 로그인 API 확인해줘"

AI 동작:
1. ~/.claude/config/projects.yaml에서 "ERP서버" 별칭 검색
2. WooriErp 프로젝트 (path: /Users/.../WooriErp) 확인
3. 해당 경로의 PROJECT_STRUCTURE.md 참조 (있으면)
4. Controllers/에서 로그인 관련 API 탐색
```

---

## 관련 명령어

| 명령어 | 설명 |
|--------|------|
| `/project:structure` | 프로젝트 상세 구조 분석 문서 생성 |
| `/project:new` | 새 프로젝트 생성 |
