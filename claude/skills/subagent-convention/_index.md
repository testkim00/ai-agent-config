# 오케스트레이션 문서 인덱스

> **오케스트레이션 시작 시 반드시 확인**
>
> 1. 이 파일(`_index.md`) 확인
> 2. `instruction.md` 읽기 (5단계 흐름 숙지)
> 3. 1단계부터 시간 기록 시작

## 문서 구조

```
~/.claude/
├── commands/
│   └── orchestration.md       ← 커맨드 레퍼런스 (사용법, 예시)
└── skills/subagent-convention/
    ├── _index.md              ← 현재 파일 (문서 인덱스)
    ├── instruction.md         ← 핵심 규칙 (5단계 흐름)
    ├── config.md              ← 모델/설정
    └── templates/
        ├── setter.md          ← 정보 수집 템플릿
        ├── executor.md        ← 실행자 템플릿
        ├── file-processor.md  ← 파일 처리 템플릿
        ├── analyzer.md        ← JSON 스키마, 병목 분석
        ├── execution-report.md← 콘솔 보고서 템플릿
        ├── api-caller.md      ← API 호출 템플릿
        └── codex-caller.md    ← Codex 호출 템플릿
```

## 필수 확인 파일

| 우선순위 | 파일 | 용도 |
|---------|------|------|
| ⭐ 1 | `instruction.md` | 5단계 흐름, 역할 정의, 핵심 원칙 |
| ⭐ 2 | `config.md` | 모델 설정 (Opus/Sonnet) |
| ⭐ 3 | `templates/analyzer.md` | JSON 스키마, 병목 분석 |
| ⭐ 3 | `templates/execution-report.md` | 콘솔 보고서 형식 |

## 수정 가이드

| 수정 대상 | 영향 파일 |
|----------|----------|
| 흐름/단계 변경 | instruction.md → analyzer.md → execution-report.md |
| 역할 추가/변경 | instruction.md → config.md → 해당 templates/*.md |
| 보고서 형식 변경 | execution-report.md (콘솔) + analyzer.md (JSON) |

## 관련 외부 문서

| 파일 | 관계 |
|------|------|
| `~/.claude/CLAUDE.md` | 위임 체계 요약 (상위 참조) |
| `~/.claude/orchestration/reports/` | JSON 보고서 저장 위치 |
