# Subagent 설정

> 모델/명령 변경 시 이 파일만 수정

## 기본 설정

```
DEFAULT_MODEL: sonnet
DEFAULT_SUBAGENT_TYPE: Bash
```

## Codex 설정

```
CODEX_COMMAND: codex exec
CODEX_DEFAULT_MODE: --full-auto
CODEX_NETWORK_MODE: --sandbox danger-full-access
```

## 모델 옵션

| 모델 | 특징 | 용도 |
|------|------|------|
| `haiku` | 빠름, 저비용 | 매우 단순한 작업 |
| `sonnet` | 균형 (기본값) | 대부분의 실행 작업 |
| `opus` | 고성능 | 복잡한 판단 |

## 역할별 모델 매핑

| 역할 | 모델 | subagent_type |
|------|------|---------------|
| Orchestrator | Opus | - (메인) |
| Setter | Sonnet | Explore |
| Advisor | Codex | - (외부) |
| Supervisor | Opus | general-purpose |
| Executor | Sonnet | general-purpose |
| Analyzer | Sonnet | general-purpose |

## 변경 이력

| 날짜 | 변경 |
|------|------|
| 2026-01-19 | 초기 설정 |
