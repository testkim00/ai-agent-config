# Project Memo

세션 작업 내용을 도메인 단위로 축약 저장. 코드의 주석 역할.

## 사용법

```
/project:memo <도메인키워드>             # 해당 도메인 작업 내용 저장/갱신
/project:memo <도메인키워드> <보충설명>   # 보충 설명 포함
/project:memo                           # 세션 전체 자동 요약
/project:memo --list                    # 저장된 메모 목록
/project:memo --show <도메인키워드>      # 특정 메모 확인
/project:memo --remove <도메인키워드>    # 메모 삭제
```

## 핵심 원칙

1. **인덱스 기반 중복 방지**: MEMORY.md를 먼저 탐색. 같은 도메인 파일은 절대 2개 이상 만들지 않는다.
2. **간결함**: 메모 1개당 30줄 이내. 장황한 설명 금지.
3. **세션에서 언급된 것만**: 대화에서 언급되지 않은 내용은 추측해서 넣지 않는다.
4. **주석 역할**: "어디에 무엇이 있고, 뭘 주의해야 하는가"만 기록.

## 처리 흐름

```
1단계: MEMORY.md 인덱스 탐색 (중복 방지)
  ├ 정확히 일치 → 기존 파일 업데이트
  ├ 유사 항목 → 사용자에게 병합 여부 확인
  └ 없음 → 신규 생성

2단계: 세션 대화 분석 (언급된 것만 수집)
  ├ 용어 정리: 사용자가 부르는 이름 ↔ 실제 파일/테이블 매핑
  ├ 관련 파일: Controller, Service, Model 각각의 용도
  ├ DB 테이블: 테이블명, 키 구성, 어떤 DbContext인지
  ├ 주의사항: 작업 중 발견한 함정, 사용자가 주의하라고 한 것
  └ 미완료: 다음에 이어서 할 작업 (있을 때만)

3단계: 저장
  ├ memory/project_{도메인키}.md 작성/갱신
  └ MEMORY.md 인덱스 동기화
```

## 메모 파일 형식

```markdown
---
name: project_{도메인키}
description: {1줄 요약}
type: project
---

## 용어
- "그룹권한" → GroupService.cs + DataPlatformGroupPermission 테이블

## 파일 → 용도
- Services/Admin/GroupService.cs → 그룹 CRUD + 권한 매핑
- Controllers/Admin/GroupManageController.cs → 그룹 관리 API

## 테이블 → 용도
- WooriCore: DataPlatformGroups(GroupId) → 그룹 마스터
- WooriCore: DataPlatformGroupPermission(GroupId+MenuId) → 그룹별 메뉴 권한

## 주의사항
- 고정 그룹 3개는 삭제 불가

## 작업 이력
- 2026-03-20: 그룹권한 리팩토링
```

**섹션 규칙:**
- 세션에서 언급된 섹션만 포함 (빈 섹션 만들지 않음)
- 용어: 사용자가 부르는 이름과 실제 코드/테이블 간 매핑
- 파일 → 용도: Controller, Service, Model 각각 1줄
- 테이블 → 용도: DbContext 명시, 키 구성 (복합키는 반드시 표기)
- 주의사항: 함정, 제약, 순서 의존성 등
- 작업 이력: 날짜 + 1줄 요약

## 중복 방지 규칙

| 상황 | 처리 |
|------|------|
| 도메인 키워드 정확히 일치 | 기존 파일 업데이트 (새 정보만 병합) |
| 유사 키워드 (예: "그룹" vs "그룹권한") | 사용자에게 확인 |
| 없음 | 신규 생성 |

**업데이트 시:**
- 새로운 정보만 추가
- 오래된/무효 정보 제거
- 작업 이력에 새 항목 추가

## MEMORY.md 인덱스

**위치:** `~/.claude/projects/{프로젝트ID}/memory/MEMORY.md`

```markdown
# Memory Index

| 도메인 | 파일 | 설명 | 최종 수정 |
|--------|------|------|----------|
| 그룹권한 | project_그룹권한.md | 그룹 CRUD, 권한 매핑 | 2026-03-20 |
```

## 금지 사항

- 코드 블록 저장 금지 (경로와 키워드만)
- 민감 정보 (비밀번호, 연결 문자열, API 키) 저장 금지
- 세션에서 언급 안 된 내용 추측 저장 금지
- 동일 도메인 파일 2개 이상 생성 금지

ARGUMENTS: $ARGUMENTS
