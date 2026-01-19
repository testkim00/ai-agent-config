# Subagent Convention

## 핵심 원칙

```
계획/검토 → Opus (직접)
단순 반복 → Sonnet (위임)
자문/검토 → Codex (동료)
독립 작업 → 병렬 실행
```

## 위임 체계

| 대상 | 모델 | 역할 | 특징 |
|------|------|------|------|
| **Orchestrator** | Opus | 오케스트레이션 | 계획 수립, 검토, 복잡한 판단 |
| **Setter** | Sonnet | 정보 수집 | 파일 경로, API 주소, 문서 등 세팅 |
| **Executor** | Sonnet | 실행 | 단순 반복 작업 |
| **Codex** | - | 자문 | 동등 수준 동료, 계획 검토, 전문 분야 |

### Setter 역할

Orchestrator가 상세 계획을 수립하기 전에 필요한 정보를 수집:

- 관련 파일 경로 탐색
- API 엔드포인트 확인
- 참고 문서 위치
- 기존 코드 패턴 파악
- 의존성 확인

```
[흐름]
사용자 요청 → Setter(정보 수집) → Orchestrator(계획 수립) → Executor(실행)
```

## 위임 기준

### 유형별

| 유형 | 처리 |
|------|------|
| 단순 반복 | ✅ Sonnet |
| 복잡한 판단 | ❌ 직접 |
| 계획 검토/자문 | ✅ Codex |

### 작업량별

> subagent 생성 비용 > 실행 비용이면 직접 처리

| 작업량 | 처리 |
|--------|------|
| 1~2개 | 직접 실행 |
| 3개 이상 | 병렬 위임 |

## 병렬 실행

### 조건

| 조건 | 병렬 |
|------|------|
| 의존성 없음 | ✅ |
| 결과 의존 | ❌ |
| 같은 파일 수정 | ❌ |

### 방법

```python
# 한 메시지에 여러 Task = 병렬
Task(model="sonnet", prompt="작업 A")
Task(model="sonnet", prompt="작업 B")
```

## Task 호출

```python
Task(
    subagent_type="Bash",
    model="sonnet",  # config.md 참조
    prompt="""
    [작업명]:
    [입력]: ...
    [처리]: 1. ... 2. ...
    [출력]: 성공/실패, 결과
    """
)
```

## Codex 호출

```bash
# 기본
codex exec "{프롬프트}" --full-auto

# 네트워크 필요
codex exec "{프롬프트}" --sandbox danger-full-access
```

## 템플릿

| 템플릿 | 용도 |
|--------|------|
| `executor.md` | git, shell 명령 |
| `file-processor.md` | 파일 처리 |
| `api-caller.md` | API 호출 |
| `codex-caller.md` | Codex 호출 |

## 참고

- 설정: [config.md](./config.md)
- 템플릿: [templates/](./templates/)
