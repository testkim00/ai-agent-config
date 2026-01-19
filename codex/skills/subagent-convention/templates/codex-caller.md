# Codex Caller Template

Codex CLI 호출용 subagent 템플릿

## Codex란?

> **Codex는 Opus와 동등한 수준의 AI다. 단순 반복 작업용이 아니다.**

OpenAI Codex CLI - 복잡한 계획 검토, 전문 분야 자문, 실시간 정보 조회에 활용

## 템플릿

```python
Task(
    subagent_type="Bash",
    model="sonnet",  # config.md 참조
    prompt="""
    Codex 호출 작업:

    [요청]: {작업 내용}
    [샌드박스]: {basic/full-access}

    [처리 단계]:
    1. Codex 명령 구성
       - 기본: codex exec "{프롬프트}" --full-auto
       - 네트워크 필요: codex exec "{프롬프트}" --sandbox danger-full-access

    2. 실행 및 결과 캡처

    3. 결과 반환
       - 성공 시 출력 내용
       - 실패 시 에러 메시지

    [출력]:
    - Codex 실행 결과
    - 성공/실패 여부
    """
)
```

## 사용 예시

### 기본 실행 (네트워크 제한)

```python
Task(
    subagent_type="Bash",
    model="sonnet",
    prompt="""
    Codex 호출:

    요청: 현재 프로젝트의 코드 품질 분석

    실행:
    codex exec "이 프로젝트의 코드 품질을 분석하고 개선점을 제안해줘" --full-auto

    결과 반환
    """
)
```

### 네트워크 필요 (외부 API, 웹 검색)

```python
Task(
    subagent_type="Bash",
    model="sonnet",
    prompt="""
    Codex 호출:

    요청: 현재 환율 조회

    실행:
    codex exec "현재 USD/KRW 환율을 조회해줘" --sandbox danger-full-access

    결과 반환
    """
)
```

## 언제 Codex를 사용하나?

| 상황 | Codex 사용 |
|------|-----------|
| 복잡한 계획 검토/재검토 | ✅ |
| 잘 모르는 분야 자문 | ✅ |
| 대규모 코드 리팩토링 | ✅ |
| 최신 프레임워크 패턴 적용 | ✅ |
| 단순 파일 작업 | ❌ (Sonnet 사용) |
| 복잡한 판단 (내가 할 수 있는 것) | ❌ (Opus 직접) |

## 샌드박스 옵션

| 옵션 | 사용 상황 |
|------|----------|
| `--full-auto` (기본) | 로컬 작업, 네트워크 불필요 |
| `--sandbox danger-full-access` | 외부 API, 웹 검색 필요 |

## 주의사항

- Codex 응답은 항상 검토 후 사용자에게 전달
- 네트워크 작업은 반드시 `--sandbox danger-full-access` 사용
- Codex 실패 시 대안 제시
