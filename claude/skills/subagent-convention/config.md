# Subagent 설정

> 모델/명령 변경 시 이 파일만 수정

## 계층별 모델 설정

```
ORCHESTRATOR: opus (직접 - subagent 아님)
SUPERVISOR: opus
EXECUTOR: sonnet
SIMPLE_EXECUTOR: haiku
```

## 역할별 subagent_type

```
SUPERVISOR_TYPE: general-purpose
EXECUTOR_TYPE: Bash
```

## Codex 설정

```
CODEX_COMMAND: codex exec
CODEX_DEFAULT_MODE: --full-auto
CODEX_NETWORK_MODE: --sandbox danger-full-access
```

## 모델 옵션

| 모델 | 계층 | 특징 | 용도 |
|------|------|------|------|
| `opus` | 감독관 | 고성능 | 복잡한 판단, 재위임 결정 |
| `sonnet` | 실행자 | 균형 | 대부분의 실행 작업 |
| `haiku` | 실행자 | 빠름, 저비용 | 매우 단순한 작업 |

## 변경 이력

| 날짜 | 변경 |
|------|------|
| 2026-01-19 | 3계층 구조로 변경 (오케스트레이터-감독관-실행자) |
| 2026-01-19 | 초기 설정 |
