# Subagent Convention Index

> **Subagent 관련 문서를 수정하거나 delegation 규칙을 바꿀 때 먼저 확인**
>
> 1. 이 파일(`_index.md`) 확인
> 2. `instruction.md` 읽기
> 3. `config.md`와 관련 template 범위 확인

## 문서 구조

```text
codex/
├── _relations.yaml
├── AGENTS.md
└── skills/subagent-convention/
    ├── _index.md
    ├── instruction.md
    ├── config.md
    └── templates/
        ├── api-caller.md
        ├── codex-caller.md
        ├── executor.md
        └── file-processor.md
```

## 필수 확인 파일

| 우선순위 | 파일 | 용도 |
|---------|------|------|
| ⭐ 1 | `instruction.md` | delegation 기준, 역할, wait 규칙 |
| ⭐ 2 | `config.md` | 모델/호출 기본 설정 |
| ⭐ 3 | `templates/*.md` | caller/worker 프롬프트 템플릿 |

## 수정 가이드

| 수정 대상 | 영향 파일 |
|----------|----------|
| delegation 기준 변경 | `instruction.md` → 관련 `templates/*.md` |
| 역할/모델 설정 변경 | `config.md` → 관련 `templates/*.md` |
| caller 템플릿 변경 | 해당 `templates/*.md` + `instruction.md` |

## 관련 외부 문서

| 파일 | 관계 |
|------|------|
| `/Users/honeychaser/Projects/ai-agent-config/codex/_relations.yaml` | Codex 전체 관계 인덱스 |
| `/Users/honeychaser/Projects/ai-agent-config/codex/AGENTS.md` | Codex 공통 실행 규칙 |
