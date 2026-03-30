# Migration Document Set

Use this reference when the task is to produce the full migration doc pack for a legacy `WERPBiz` module.

## Required outputs

Create a module-specific folder such as `docs/<module>-migration/`.

Minimum document set:

1. `README.md`
2. `01-menu-structure.md`
3. `02-screen-catalog.md`
4. `03-main-screens.md`
5. `04-popup-screens.md`
6. `05-navigation-flow.md`
7. `06-procedure-and-data-contracts.md`
8. `07-web-migration-design.md`
9. `08-target-project-fit.md`
10. `09-implementation-blueprint.md`

Add DB-backed docs when possible:

11. `10-werpbiz-procedures-and-tables.md`
12. `db/README.md`
13. raw CSV and SQL exports under `db/`

## What each document must cover

### `README.md`

- 목적
- 분석 범위
- source-of-truth priority
- 문서 목록
- 핵심 결론
- 권장 사용 순서
- 추가 확인 필요 항목

### `01-menu-structure.md`

- 현재 WinForms 메뉴 트리
- 메뉴 진입점
- 숨김/권한/관리자 전용 기능

### `02-screen-catalog.md`

- 전체 화면 목록
- 현재 역할
- 목표 웹 화면 분리안

### `03-main-screens.md`

- 메인 화면별 필터, 버튼, grid, 탭, 저장 흐름
- 조회/관리/집계/보조기능 구분

### `04-popup-screens.md`

- 팝업 목적
- 부모 화면
- 입력/선택/저장 기능
- 상위 화면 반영 방식

### `05-navigation-flow.md`

- 현재 화면 이동 흐름
- 부모-자식 화면 콜백
- 웹 라우트/모달 분리 기준

### `06-procedure-and-data-contracts.md`

- 화면 기준 저장/조회 프로시저 맵
- 탭과 work type 매핑
- aggregate 후보
- 파일/암호화/외부 API 규칙

### `07-web-migration-design.md`

- Vue 3 + .NET 기준 목표 구조
- 화면 분리 원칙
- API/서비스/상태관리 방향
- 성능/보안 개선안

### `08-target-project-fit.md`

- 실제 `WooriErpClient` 구조와 맞는지
- 실제 `WooriErp` 구조와 맞는지
- 파일 배치, 라우팅, DTO, 서비스 패턴

### `09-implementation-blueprint.md`

- 구현자가 바로 코드 작성 가능한 수준의 파일 위치
- menu key/view name
- controller/service/dto/entity/query 단위
- 단계별 구현 순서

### `10-werpbiz-procedures-and-tables.md`

- live DB 기준 프로시저 그룹
- 주요 work type 분기
- 핵심 테이블과 row count
- 타입 불일치, PK 리스크
- side effect, transaction boundary 시사점

## Writing rules

- 소스 코드 설명이 아니라 구현 지침 문서로 쓴다.
- confirmed fact와 inference를 섞지 않는다.
- “웹에서는 어떻게 분리해야 하는가”를 항상 같이 적는다.
- 다른 AI가 읽고 바로 구현할 수 있는 수준까지 구체화한다.
