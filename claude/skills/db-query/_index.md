# DB 쿼리 스킬 인덱스

> **수정 시 필수 확인**
>
> DB 쿼리 스킬 수정 전:
> 1. 이 파일의 관련 문서 목록 확인
> 2. 스키마 변경 시 schema/*.md 일관성 확인
> 3. 관련 커맨드 (`/db:query`, `/db:convert`) 확인

## 문서 구조

```
skills/db-query/
├── _index.md           ← 현재 파일
├── skill.md            ← 쿼리 실행 가이드
├── databases.md        ← DB 연결 정보
├── templates.md        ← 쿼리 템플릿
└── schema/             ← 테이블 스키마
    ├── _summary.md     ← 스키마 요약
    └── WERPBiz.md      ← WERPBiz DB 스키마
```

## 문서 목록

| 파일 | 설명 | 관련 |
|------|------|------|
| `skill.md` | 쿼리 실행 방법, 권한 | 커맨드 |
| `databases.md` | DB 연결 문자열, 권한 | 환경 |
| `templates.md` | 자주 쓰는 쿼리 템플릿 | 업무 |
| `schema/_summary.md` | DB별 테이블 요약 | 스키마 |
| `schema/WERPBiz.md` | WERPBiz 상세 스키마 | 스키마 |

## 관련 커맨드

| 커맨드 | 경로 | 역할 |
|--------|------|------|
| `/db:query` | `commands/db/query.md` | 쿼리 실행 |
| `/db:convert` | `commands/db/convert.md` | 결과 변환 |

## 수정 시 체크리스트

### 스키마 변경

- [ ] `schema/{db}.md` 수정
- [ ] `schema/_summary.md` 업데이트
- [ ] `templates.md` 쿼리 유효성 확인

### 새 DB 추가

- [ ] `databases.md` 연결 정보 추가
- [ ] `schema/{db}.md` 스키마 문서 생성
- [ ] `schema/_summary.md` 업데이트
- [ ] 이 파일 업데이트

### 쿼리 템플릿 추가

- [ ] `templates.md` 템플릿 추가
- [ ] 스키마 참조 정확성 확인

### 실행 방식 변경

- [ ] `skill.md` 수정
- [ ] `commands/db/query.md` 동기화

## 의존성 관계

```
commands/db/query.md
    │
    ├──► skill.md (실행 방법)
    ├──► databases.md (연결 정보)
    └──► templates.md (템플릿)

commands/db/convert.md
    │
    └──► skill.md (출력 형식)

templates.md
    │
    └──► schema/*.md (테이블 참조)
```
