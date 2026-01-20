# DB 커맨드 인덱스

> **수정 시 필수 확인**
>
> DB 커맨드 수정 전:
> 1. 이 파일의 관련 문서 목록 확인
> 2. `skills/db-query/_index.md` 확인
> 3. 스키마 정보, 템플릿과 일관성 유지

## 문서 구조

```
commands/db/
├── _index.md       ← 현재 파일
├── query.md        ← 쿼리 실행
└── convert.md      ← 결과 변환
```

## 커맨드 목록

| 커맨드 | 파일 | 설명 |
|--------|------|------|
| `/db:query` | `query.md` | DB 쿼리 실행 및 결과 반환 |
| `/db:convert` | `convert.md` | 쿼리 결과 형식 변환 |

## 관련 스킬

| 스킬 | 경로 | 역할 |
|------|------|------|
| DB 쿼리 | `skills/db-query/_index.md` | 스킬 인덱스 |
| | `skills/db-query/skill.md` | 쿼리 실행 가이드 |
| | `skills/db-query/databases.md` | DB 연결 정보 |
| | `skills/db-query/templates.md` | 쿼리 템플릿 |
| | `skills/db-query/schema/*.md` | 테이블 스키마 |

## 수정 시 체크리스트

- [ ] 쿼리 실행 방식 변경 → `query.md`, `skill.md` 함께 수정
- [ ] 출력 형식 변경 → `convert.md` 수정
- [ ] 새 DB 추가 → `databases.md`, 스키마 파일 추가
- [ ] 새 템플릿 추가 → `templates.md` 수정
