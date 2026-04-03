---
name: harness
description: Repo별 `.codex/harness.json` 기본 harness를 조회, 생성, 수정, 리뷰할 때 사용한다. 여러 저장소의 harness 목록을 보고 싶거나, 특정 repo의 stack과 검증 명령에 맞는 기본 harness를 만들거나, 기존 harness가 과도하거나 부족한지 다듬고 싶을 때 사용한다.
---

# Harness

## 언제 사용하나

- 사용자가 repo 기본 harness를 만들거나 바꾸고 싶을 때
- 여러 repo의 harness 존재 여부와 강제 상태를 한 번에 보고 싶을 때
- 특정 repo에 맞는 `required_all`, `required_any`, `skip_turn_types`를 정하고 싶을 때
- 기존 harness가 너무 느슨하거나 너무 빡빡해서 조정이 필요할 때

## 핵심 해석

- 이 스킬의 대상은 repo root의 `.codex/harness.json` 이다.
- 공통 규칙은 preset으로 모듈화하고, repo별 `.codex/harness.json` 에서는 그 preset을 선택한 뒤 필요한 override만 남기는 구조를 우선한다.
- 목적은 `무조건 테스트`가 아니라 `repo에 맞는 적절한 검증을 기본값으로 강제`하는 것이다.
- generic 템플릿을 그대로 복사하지 않는다.
- repo마다 stack, 실행 명령, 실패 비용, CI 관례가 다르므로 매번 맞춤형으로 설계한다.

## preset 구조

- 공통 harness preset 파일은 `/Users/honeychaser/Projects/ai-agent-config/codex/skills/harness/presets/` 아래에 둔다.
- 예:
  - `frontend-quasar`
  - `frontend-nuxt`
  - `backend-dotnet`
  - `desktop-winforms`
  - `python-service`
  - `tooling-config`
- hook은 repo의 `.codex/harness.json` 에 `preset` 이 있으면 preset을 먼저 읽고, 그 다음 repo 파일의 override를 덮어쓴다.
- 따라서 새 repo를 만들 때는 가능하면 아래처럼 시작한다.

```json
{
  "version": 1,
  "preset": "frontend-quasar",
  "name": "MyRepo-default",
  "description": "Repo-specific default harness for MyRepo."
}
```

- 특정 repo만 다른 점이 있으면 그때만 override를 추가한다.
  - `required_all`
  - `required_any`
  - `unsupported_platforms`
  - `consistency_check.enabled`

## 먼저 할 일

1. 대상 repo가 하나인지 여러 개인지 정한다.
2. 여러 repo면 목록부터 본다.
3. 대상 repo면 기존 harness, manifest, 테스트 명령, CI 힌트부터 읽는다.

## 번들 스크립트

- 목록 조회: `/Users/honeychaser/Projects/ai-agent-config/codex/skills/harness/scripts/list_repo_harnesses.py`
- repo별 추천안 생성: `/Users/honeychaser/Projects/ai-agent-config/codex/skills/harness/scripts/suggest_repo_harness.py`

기본 예시:

```bash
python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/harness/scripts/list_repo_harnesses.py /Users/honeychaser/Projects
python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/harness/scripts/suggest_repo_harness.py --repo /path/to/repo
python3 /Users/honeychaser/Projects/ai-agent-config/codex/skills/harness/scripts/suggest_repo_harness.py --repo /path/to/repo --format json
```

## 기본 흐름

### 1. 목록 조회

- 여러 repo를 다루면 먼저 목록 스크립트로 harness 존재 여부를 본다.
- 보고 싶은 기준은 최소 아래다.
  - harness 파일 존재 여부
  - `enforce` 여부
  - `required_all` / `required_any` 개수
  - JSON 파싱 오류 여부

### 2. 대상 repo 분석

- 아래 파일을 우선 본다.
  - `.codex/harness.json`
  - `AGENTS.md`
  - `README.md`
  - `package.json`
  - `pyproject.toml`
  - `Cargo.toml`
  - `go.mod`
  - `pom.xml`
  - `build.gradle*`
  - `*.sln`, `*.csproj`
  - `.github/workflows/*.yml`
- 추천 스크립트는 초기 초안을 만드는 용도다.
- 최종 harness는 반드시 repo 실제 명령과 운영 비용을 보고 수동 조정한다.

### 3. harness 설계

- 기본값:
  - 가능하면 공통 preset에서 가져온다.
  - repo 파일에는 차이만 남긴다.
- 하지만 repo가 docs-only에 가깝거나 검증 비용이 비정상적으로 크면 그대로 두지 말고 조정한다.
- 로컬 OS에서 아예 불가능한 검증이면 아래 플랫폼 제약도 같이 둔다.
  - `unsupported_platforms`: 이 환경에서는 stop hook이 하드 강제하지 않을 플랫폼 목록
  - `unsupported_platform_reason`: 왜 여기서는 강제를 풀어야 하는지 설명
- 예:
  - legacy WinForms/.NET Framework desktop repo는 macOS에서 빌드 검증이 불가능할 수 있으므로 `unsupported_platforms: ["darwin"]` 를 둔다.

### 3-1. `consistency_check` 강제 규칙

- 제품 repo에는 검증 matcher만 넣지 말고 `consistency_check` 항목도 같이 둔다.
- 목적은 미적인 취향 검사가 아니라 `기존 화면/API/module 패턴을 먼저 참조했는지`를 stop hook에서 실제로 강제하는 것이다.
- 이 항목은 보통 아래를 포함한다.
  - `profile`: repo 유형
  - `summary`: 이 repo에서 무엇의 일관성을 가장 먼저 볼지
  - `applies_to`: 어떤 파일군에 우선 적용할지
  - `reference_expectation`: 최종 보고에서 남겨야 할 reference 힌트
  - `required_checklist`: 반드시 포함할 기준 문구
  - `project_notes`: repo별 해석 주석
- `required_checklist`에는 최소 아래 다섯 문구를 그대로 넣는다.
  - `같은 계열 기존 화면(혹은 API) 2~3개를 reference로 잡았는지`
  - `최대한 기존의 공통 wrapper/layout/component/module 등을 활용하는지`
  - `inline color, inline spacing, local-only radius 같은 임의 스타일을 넣지 않았는지`
  - `(shared) component import 패턴이 기존과 맞는지`
  - `grid/list/form 화면별로 정해둔 기본 구조를 벗어났는지`
- 단, repo가 frontend가 아니면 UI 문구를 그대로 지우지 말고 `project_notes`에서 API/module/job 구조에 대응시켜 해석한다고 명시한다.
- 특정 repo를 예외로 둘 필요가 있으면 `consistency_check`를 생략하거나 `enabled: false`로 남긴다.
- 현재 local hook 기준으로는 consistency 범위 파일이 바뀐 turn에서 최종 응답에 아래 형식이 없으면 stop이 통과하지 않는다.
  - `CONSISTENCY_CHECK:`
  - `References: 실제 존재하는 파일 경로 2~3개`
  - `Reuse: 재사용한 구체 component/module/import 이름`
  - `Checklist: ok - 기존 패턴 유지`
- `References:`는 현재 repo 안의 실제 파일이어야 한다. absolute path 또는 repo-relative path를 쓰되, 존재하지 않는 경로나 설명용 이름만 적으면 stop이 막힌다.
- `Reuse:`는 `wrapper`, `layout`, `component` 같은 일반명사만 적으면 통과하지 않는다. `BasePage`, `DataToolBar`, `useAuthStore`, `SearchFormLayout`처럼 구체 이름을 적는다.

### 4. `required_all` / `required_any` 결정

- `required_all`:
  - 빠르고 안정적이고 거의 항상 가능한 검증만 넣는다.
  - 예: `tag:lint`, `tag:typecheck`, `tag:check`
- `required_any`:
  - heavier validation이나 상황별 검증을 넣는다.
  - 예: `tag:test`, `tag:build`, `command:<regex>`
- rule of thumb:
  - 프론트엔드/TS repo: 보통 `lint + typecheck`를 강하게 보고 `test/build` 중 하나를 추가로 허용한다.
  - Python repo: 실제로 존재하는 `ruff/flake8`, `mypy/pyright`, `pytest`, `py_compile` 중 가능한 조합을 고른다.
  - .NET/Java/Go/Rust repo: repo에서 실제로 돌리는 `build/test/check/lint` 조합을 우선한다.
  - shell-heavy repo: `sh -n`, `shellcheck` 같은 저비용 검증을 우선한다.

## override 원칙

- preset에 이미 들어 있는 값을 repo 파일에 중복으로 다시 쓰지 않는다.
- repo 파일에는 아래처럼 `왜 이 repo만 다른지`가 드러나는 차이만 남긴다.
  - 특정 build 명령 추가
  - consistency 예외
  - unsupported platform
  - heavier `required_all`
- 예:

```json
{
  "version": 1,
  "preset": "backend-dotnet",
  "name": "ApiHub-default",
  "description": "Repo-specific default harness for ApiHub.",
  "consistency_check": {
    "enabled": false
  }
}
```

## 하지 말아야 할 것

- 모든 repo에 같은 harness를 복붙하지 않는다.
- preset이 있는데 repo마다 같은 JSON을 길게 중복 생성하지 않는다.
- 존재하지 않는 명령을 required matcher로 강제하지 않는다.
- `required_all`에 무거운 검증을 너무 많이 넣지 않는다.
- docs-only 변경까지 풀 검증을 강제하지 않는다.
- CI에서만 가능한 검증을 로컬 기본 harness에 무심코 넣지 않는다.

## 수정 원칙

- 기존 harness가 너무 약하면 `required_any`만 늘리지 말고 `required_all`도 재평가한다.
- 기존 harness가 너무 자주 막으면 `required_all`을 줄이고 `required_any`로 내릴지 본다.
- repo가 mixed stack이면 한 언어 기준으로 단정하지 말고, 실제 수정이 자주 일어나는 경로 기준으로 본다.
- hook 분류기가 이미 인식하는 태그를 우선 사용하고, 부족할 때만 `command:<regex>`를 쓴다.
- `consistency_check`는 repo 이름만 바꿔 복붙하지 말고, 실제 stack과 주 수정 경로에 맞게 `summary`, `applies_to`, `project_notes`를 바꾼다.

## 결과 검증

- `.codex/harness.json` JSON 파싱 확인
- preset을 쓰는 경우 preset 이름이 실제 존재하는지 확인
- 가능하면 repo 대표 검증 명령이 실제로 존재하는지 확인
- 필요하면 `git diff --check`
- hook 강제와 충돌하는 과도한 설정이 아닌지 다시 본다

### 최종 검증 재시도 규칙

- 최종 검증이 실패하면 바로 포기하지 말고 원인을 좁혀서 수정 후 다시 검증한다.
- 이 재시도는 `최대 5회`까지만 한다.
- 매 재시도에서는 무엇을 바꿨고 어떤 검증을 다시 돌렸는지 짧게 추적한다.
- `5회` 안에 해결되지 않으면 더 추측하지 말고 멈춘다.
- 그 경우 사용자에게 아래를 짧게 알리고 도움을 요청한다.
  - 어떤 검증이 계속 실패하는지
  - 지금까지 무엇을 시도했는지
  - 어떤 추가 정보나 결정이 필요한지
- 사용자가 명시적으로 더 밀어붙이라고 하지 않은 한, 실패 상태를 숨기거나 억지로 `HARNESS_SKIP:`로 넘기지 않는다.

## 결과 보고

- 어떤 repo를 대상으로 했는지
- 기존 harness가 있었는지
- 무엇을 왜 바꿨는지
- 이제 어떤 검증이 기본 강제되는지
- 예외로 남겨둔 부분이 무엇인지
