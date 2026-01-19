# Subagent Convention

## 4계층 위임 체계

```
오케스트레이터 (Opus)
    │ 세분화된 작업 위임
    ▼
감독관 (Opus subagent)
    │ 단순 반복 업무 위임
    ▼
실행자 (Sonnet subagent)
```

**계획 수립 단계 전용 도구:**
- Setter (Sonnet) - 정보 수집: 파일 경로, API 엔드포인트, 기존 패턴, 의존성
- Advisor (Codex) - 계획 검토, 전문 분야 자문 (⚠️ 계획 단계에서만 사용)

## 역할 요약

| 대상 | 모델 | 역할 |
|------|------|------|
| Orchestrator | Opus | 상세 계획 수립, 복잡한 판단 |
| Setter | Sonnet | 정보 수집 (계획 단계) |
| Advisor | Codex | 계획 검토 (계획 단계만) |
| Supervisor | Opus subagent | 작업 책임, 검수, 재위임 |
| Executor | Sonnet | 단순 반복 실행 |

## 작업 흐름

```
[계획 수립 단계]
사용자 요청 → Setter(정보 수집) → 초안 계획
           → 추가 정보 필요? → Setter(추가 수집)
           → Advisor(계획 검토) → 상세 계획 확정

[실행 단계]
Supervisor(작업 관리) → Executor(병렬 실행) → 결과 취합
```

## 상세 계획 포맷

```markdown
## 상세 계획

### 1. 목표
- 최종 목표: {목표}
- 성공 기준: {기준}

### 2. 작업 분할

| 작업 ID | 작업 내용 | 담당 | 의존성 | 병렬 가능 |
|---------|----------|------|--------|----------|
| T1 | {작업1} | 감독관A | 없음 | O |
| T2 | {작업2} | 감독관A | T1 | X |

### 3. 병렬 처리 전략
- 1차 병렬 (감독관 레벨): 감독관A: T1, T2 / 감독관B: T3, T4
- 2차 병렬 (실행자 레벨): 각 감독관 → 실행자 N명

### 4. 의존성 순서
T1, T2 (병렬) → T3 (순차) → T4, T5 (병렬)
```

### 계획 체크리스트

- [ ] 작업이 명확하게 분할되었는가?
- [ ] 각 작업의 담당자가 지정되었는가?
- [ ] 의존성이 파악되었는가?
- [ ] 병렬 처리 가능한 작업이 식별되었는가?

## 위임 기준

| 조건 | 처리 |
|------|------|
| 단순 반복 1~2개 | 직접 실행 |
| 단순 반복 3개+ | Executor 병렬 위임 |
| 복잡한 판단 | 직접 |
| 계획 검토 | Advisor (계획 단계만) |

**병렬 실행 조건:**
- 의존성 없음
- 같은 파일 수정 아님

## 호출 예시

### Setter 호출 (정보 수집)

```python
Task(
    subagent_type="Explore",
    model="sonnet",
    prompt="""
    [정보 수집 요청]
    - 관련 파일 경로
    - API 엔드포인트
    - 기존 코드 패턴
    """
)
```

### Supervisor 호출 (작업 위임)

```python
Task(
    subagent_type="general-purpose",
    model="opus",
    prompt="""
    [작업 ID]: T1
    [작업]: {작업 내용}
    [담당 파일]: {파일 목록}
    [권한]: 단순 반복은 실행자(sonnet) 위임 가능
    """
)
```

### Executor 병렬 호출

```python
# 한 메시지에 여러 Task = 병렬 실행
Task(model="sonnet", prompt="파일A 수정: ...")
Task(model="sonnet", prompt="파일B 수정: ...")
Task(model="sonnet", prompt="파일C 수정: ...")
```

## 핵심 원칙

1. 오케스트레이터는 상세 계획 수립 후 분배
2. Setter와 반복 협력하여 정보 확보
3. Advisor는 계획 단계에서만 사용 (실행 단계 금지)
4. 감독관은 책임지고 검수
5. 실행자는 판단 없이 실행만
6. subagent 생성 비용 > 실행 비용이면 직접 처리

## 템플릿

| 템플릿 | 용도 |
|--------|------|
| `setter.md` | 정보 수집 |
| `executor.md` | git, shell 명령 |
| `file-processor.md` | 파일 처리 |

## 참고

- 설정: [config.md](./config.md)
- 템플릿: [templates/](./templates/)
