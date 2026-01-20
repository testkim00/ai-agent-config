# Setter 템플릿

오케스트레이터가 계획 수립에 필요한 정보를 수집하는 템플릿입니다.

> **참고:** 수집 항목이 3개 이상이고 독립적인 경우, Orchestrator는 여러 Setter를 병렬로 호출할 수 있습니다.

## Task 호출

```python
Task(
    subagent_type="Explore",
    model="sonnet",
    prompt="""
    [요청 분석]
    사용자 요청: {요청 내용}

    [수집할 정보]
    1. 관련 파일 경로
    2. 참고할 기존 코드/패턴
    3. API 엔드포인트 (해당 시)
    4. 파일별 import 문 (raw data)
    5. 수정 대상 파일

    [탐색 범위]
    - 프로젝트: {현재 프로젝트 경로}
    - 깊이: 필요한 만큼

    [출력 형식]
    아래 형식으로 정리:

    ## 요약
    {요청을 수행하기 위해 필요한 핵심 정보 요약}

    ## 관련 파일
    | 경로 | 역할 | 수정 필요 |
    |------|------|----------|
    | {경로} | {설명} | ✓/✗ |

    ## 참고 패턴
    - {파일}:{라인} - {패턴 설명}

    ## API/엔드포인트
    | 메서드 | 경로 | 설명 |
    |--------|------|------|
    | {GET/POST} | {경로} | {설명} |

    ## Import 문 (raw data)
    | 파일 | import 문 |
    |------|-----------|
    | {파일경로} | {import/require 문 그대로} |

    ## 의존성
    - {A} → {B}: {관계 설명}

    ## 주의사항
    - {잠재적 위험 요소나 고려사항}
    """
)
```

## 출력 예시

```markdown
## 요약
사용자 인증 기능 추가를 위해 auth 모듈 생성 및 기존 API에 미들웨어 적용 필요

## 관련 파일
| 경로 | 역할 | 수정 필요 |
|------|------|----------|
| src/api/base.ts | API 베이스 클래스 | ✓ |
| src/middleware/index.ts | 미들웨어 정의 | ✓ |
| src/models/user.ts | 사용자 모델 | ✗ (참고) |

## 참고 패턴
- src/api/base.ts:45 - 요청 인터셉터 패턴
- src/middleware/logger.ts:12 - 미들웨어 구조

## API/엔드포인트
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | /api/user/login | 기존 로그인 (참고) |

## Import 문 (raw data)
| 파일 | import 문 |
|------|-----------|
| src/api/base.ts | `import { UserModel } from '../models/user'` |
| src/middleware/index.ts | `import { logger } from './logger'` |

## 의존성
- auth 모듈 → user 모델: 사용자 정보 참조
- API 미들웨어 → auth 모듈: 인증 검증

## 주의사항
- 기존 세션 관리 방식과 충돌 가능성 확인 필요
```
