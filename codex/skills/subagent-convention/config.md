# Subagent 설정

이 디렉터리의 기준은 `Codex local-first + selective delegation`이다.

## 기본 전략

```text
MAIN_STRATEGY: local-first
READ_ONLY_PARALLEL: multi_tool_use.parallel
AGENT_GATE: explicit-user-request-required
WRITE_SCOPE_RULE: one-owner-per-file-or-module
```

## 역할 선택

| 용도 | agent_type | 권장 방식 |
|------|------------|-----------|
| 코드베이스 read-only 질문 | `explorer` | 좁은 질문, 짧은 결과 |
| 분리 가능한 구현 작업 | `worker` | 담당 파일과 검증 명령 명시 |
| 일반 보조 작업 | `default` | explorer/worker로 애매할 때만 |

## 모델 선택 원칙

- 기본값은 현재 세션 모델을 상속한다.
- 범위가 좁고 read-only인 질문은 더 작은 모델을 고려할 수 있다.
- 파일 수정, 리팩터링, 검증이 포함되면 더 강한 모델이나 기본 상속을 우선한다.
- 모델 선택보다 `작업 범위 분리`와 `write scope 통제`가 더 중요하다.

## 권장 reasoning 강도

| 상황 | 권장 reasoning |
|------|----------------|
| 좁은 코드 탐색 | `low` 또는 `medium` |
| 일반 구현 | `medium` |
| 모호한 리팩터링, 위험한 수정 | `high` |

## 운영 원칙

- 하위 에이전트 수를 불필요하게 늘리지 않는다.
- explorer는 읽기 전용에 가깝게 유지한다.
- worker는 disjoint write scope가 아닐 때 사용하지 않는다.
- 메인 에이전트는 항상 통합과 최종 판단을 책임진다.
