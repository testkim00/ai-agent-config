# Orchestration

복잡한 작업을 체계적으로 수행하기 위한 오케스트레이션 명령어입니다.

## 사용법

```
/orchestration {대상}을 {작업}하세요
/orchestration {자연어 요청}
```

## 처리 흐름

```
1. Setter (Sonnet) → 정보 수집
2. Orchestrator (Opus) → 계획 수립
3. Executor (Sonnet) → 실행
```

### 1단계: Setter - 정보 수집

Task 도구로 Sonnet을 호출하여 다음 정보 수집:

- 관련 파일 경로 탐색 (코드, 설정, 문서)
- API 엔드포인트 확인
- 기존 코드 패턴 파악
- 의존성 및 참조 관계 확인
- 프로젝트 구조 파악

```python
Task(
    subagent_type="Explore",
    model="sonnet",
    prompt="""
    [요청]: {사용자 요청}

    다음 정보를 수집하세요:
    1. 관련 파일 경로 목록
    2. 참고할 기존 코드/패턴
    3. API 엔드포인트 (해당 시)
    4. 의존성 관계
    5. 수정이 필요한 파일 목록

    [출력 형식]
    ## 관련 파일
    - {경로}: {설명}

    ## 참고 패턴
    - {파일}:{라인} - {패턴 설명}

    ## 의존성
    - {관계 설명}
    """
)
```

### 2단계: Orchestrator - 계획 수립

Setter 결과를 바탕으로 상세 실행 계획 수립:

- 작업 단계 분류
- 의존성 순서 결정
- 병렬 실행 가능 항목 식별
- 예상 위험 요소 파악

### 3단계: Executor - 실행

계획에 따라 Sonnet으로 작업 실행:

- 독립 작업은 병렬 실행
- 의존성 있는 작업은 순차 실행
- 각 단계 완료 후 검증

## 예시

```
/orchestration 사용자 인증 기능을 추가하세요

→ [Setter] 정보 수집 중...
  - 관련 파일: src/auth/, src/api/user.ts
  - 참고 패턴: src/api/base.ts의 인증 미들웨어
  - API: POST /api/auth/login, /api/auth/logout

→ [Orchestrator] 계획 수립...
  1. 인증 모델 생성 (독립)
  2. API 엔드포인트 구현 (1 의존)
  3. 미들웨어 적용 (2 의존)
  4. 테스트 작성 (3 의존)

→ [Executor] 실행 중...
  [1/4] 인증 모델 생성 ✓
  [2/4] API 엔드포인트 구현 ✓
  ...
```

## 참고

- 위임 체계: [instruction.md](~/.claude/skills/subagent-convention/instruction.md)
- 설정: [config.md](~/.claude/skills/subagent-convention/config.md)
