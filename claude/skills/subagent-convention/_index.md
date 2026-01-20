# 오케스트레이션 문서 인덱스

> **이 파일을 먼저 읽으세요.**
> 오케스트레이션 관련 지시사항 수정/추가 시 반드시 이 인덱스를 참조하여 관련 문서를 함께 업데이트하세요.

## 문서 구조

```
~/.claude/skills/subagent-convention/
├── _index.md              ← 현재 파일 (메타 인덱스)
├── instruction.md         ← 핵심 규칙 (5단계 흐름)
├── config.md              ← 모델/설정
└── templates/
    ├── setter.md          ← 정보 수집 템플릿
    ├── executor.md        ← 실행자 템플릿
    ├── file-processor.md  ← 파일 처리 템플릿
    ├── analyzer.md        ← 실행분석관 템플릿 (JSON 스키마)
    ├── execution-report.md← 결과 보고서 템플릿 (콘솔 출력)
    ├── api-caller.md      ← API 호출 템플릿
    └── codex-caller.md    ← Codex 호출 템플릿
```

## 필수 확인 파일

| 우선순위 | 파일 | 용도 | 수정 시 영향 |
|---------|------|------|-------------|
| ⭐ 1 | `instruction.md` | 5단계 흐름, 역할 정의, 핵심 원칙 | 전체 오케스트레이션 동작 |
| ⭐ 2 | `config.md` | 모델 설정 (Opus/Sonnet) | subagent 호출 |
| ⭐ 3 | `templates/analyzer.md` | 실행분석관, 시간 기록, JSON 스키마 | 5단계 보고서 |
| ⭐ 3 | `templates/execution-report.md` | 콘솔 보고서 출력 형식 | 5단계 보고서 |

## 문서별 내용 요약

### instruction.md (핵심)
- 위임 체계 (Orchestrator → Supervisor → Executor)
- **5단계 작업 흐름** (필수 숙지)
  - 1단계: 요청 분석 및 목표 설정
  - 2단계: 정보 수집 (Setter)
  - 3단계: 정보 분석 및 상세 계획 수립
  - 4단계: 실행 (Supervisor/Executor)
  - 5단계: 실행 분석 보고 (Analyzer) ← **필수**
- 역할별 책임
- 병렬 실행 전략
- 호출 예시

### config.md
- 모델 설정 (Orchestrator: Opus, Setter/Executor: Sonnet)
- subagent_type 매핑

### templates/setter.md
- 정보 수집 프롬프트 템플릿
- 출력 형식 (구조, 역할 설명, 의존성)

### templates/executor.md
- 실행자 프롬프트 템플릿
- git, shell 명령 실행

### templates/analyzer.md
- 실행분석관 역할 정의
- 시간 기록 형식: `[TIME] {단계}.{작업ID} | {START/END} | {timestamp}`
- 병목 판단 기준 (50%↑: 🔴, 30~50%: 🟡, 30%↓: 🟢)
- JSON 보고서 스키마

### templates/execution-report.md
- 콘솔 출력 보고서 템플릿
- 필수 섹션: 요약, 작업목록, 변경파일, **단계별 소요시간**, **병목분석**

## 수정 가이드

### 흐름/단계 변경 시
```
instruction.md → analyzer.md → execution-report.md
```

### 역할 추가/변경 시
```
instruction.md → config.md → 해당 templates/*.md
```

### 보고서 형식 변경 시
```
execution-report.md (콘솔) + analyzer.md (JSON)
```

### 새 템플릿 추가 시
```
1. templates/{name}.md 생성
2. instruction.md에 역할/호출 예시 추가
3. 이 파일(_index.md) 문서 구조 업데이트
```

## 관련 외부 문서

| 파일 | 위치 | 관계 |
|------|------|------|
| `CLAUDE.md` | `~/.claude/CLAUDE.md` | 위임 체계 요약 (이 문서의 상위 참조) |
| 보고서 저장 | `~/.claude/orchestration/reports/` | 5단계 JSON 보고서 저장 위치 |

## 체크리스트

오케스트레이션 관련 수정 시:

- [ ] `instruction.md` 확인/수정
- [ ] `config.md` 확인 (모델 설정 변경 시)
- [ ] 관련 `templates/*.md` 확인/수정
- [ ] `_index.md` (이 파일) 업데이트
- [ ] `~/.claude/CLAUDE.md` 동기화 필요 여부 확인
