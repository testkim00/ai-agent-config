# Orchestration

복잡한 작업을 체계적으로 수행하는 오케스트레이션 명령어입니다.

## 사용법

```
/orchestration {대상}을 {작업}하세요
/orchestration {자연어 요청}
```

## 실행 원칙

- 단계 간 사용자 확인 없이 연속 진행
- 타임스탬프만 기록하고 즉시 다음 단계로
- 5단계 보고서 출력 후 종료

## 처리 흐름 (5단계)

> **상세 규칙:** [`instruction.md`](~/.claude/skills/subagent-convention/instruction.md) 참조

| 단계 | 설명 | 담당 |
|------|------|------|
| 1단계 | 요청 분석 및 목표 설정 | Orchestrator |
| 2단계 | 정보 수집 | Setter (Sonnet) |
| 3단계 | 분석 및 계획 수립 | Orchestrator |
| 4단계 | 실행 | Supervisor/Executor |
| 5단계 | 실행 분석 보고 (필수) | Analyzer |

### 단계별 요약

**1단계 - 요청 분석**
- 요청 내용/의도 파악
- CLAUDE.md, 프로젝트 구조 확인
- 목표 설정 및 정보 수집 목록 작성

**2단계 - 정보 수집**
- Setter에게 위임 (수집 + 역할 설명)
- 독립 항목 3개+ 시 병렬 실행
- 깊은 분석 없이 raw data 수집

**3단계 - 분석 및 계획**
- 수집 정보 분석
- import 의존성 검증 (파일 이동 시)
- 상세 실행 계획 수립

**4단계 - 실행**
- 계획에 따라 작업 실행
- 독립 작업은 병렬, 의존 작업은 순차
- 빌드/실행 검증 (해당 시)

**5단계 - 실행 분석 보고** (필수)
- 시간 기록 취합
- 병목 단계 식별 및 원인 분석
- 콘솔 보고서 + JSON 저장

## 예시

```
/orchestration 사용자 인증 기능을 추가하세요

→ [1단계: 요청 분석]
  - 의도: JWT 기반 사용자 인증 시스템 구축
  - 목표: 로그인/로그아웃 API 및 인증 미들웨어 구현
  - 수집 목록: 기존 API 구조, 미들웨어 패턴, 사용자 모델

→ [2단계: 정보 수집] Setter 호출...
  (수집 결과)

→ [3단계: 분석 및 계획]
  - 상세 계획 수립
  - 작업 분할: T1(모델) → T2(API) → T3(미들웨어)

→ [4단계: 실행] Executor 호출...
  [1/3] 인증 모델 생성 ✓
  [2/3] API 엔드포인트 구현 ✓
  [3/3] 미들웨어 적용 ✓

→ [5단계: 분석 보고]
  ═══════════════════════════════════════
              실행 분석 보고서
  ═══════════════════════════════════════
  ■ 요약
  │ 총 실행 시간: 3분 45초
  │ 병목 단계: 2단계 (정보 수집)
  ...
```

## 참고 문서

| 문서 | 용도 |
|------|------|
| [`instruction.md`](~/.claude/skills/subagent-convention/instruction.md) | 5단계 흐름, 역할 정의, 핵심 원칙 |
| [`config.md`](~/.claude/skills/subagent-convention/config.md) | 모델 설정 (Opus/Sonnet) |
| [`templates/`](~/.claude/skills/subagent-convention/templates/) | 호출 템플릿 (setter, executor, analyzer) |
