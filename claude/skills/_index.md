# 스킬 마스터 인덱스

> **스킬 수정 시 필수 확인**
>
> 스킬 파일 수정 전 반드시:
> 1. 해당 스킬의 `_index.md` 확인
> 2. 관련 커맨드가 있으면 커맨드 문서도 확인
> 3. 일관성 있게 수정

## 스킬 구조

```
skills/
├── _index.md                  ← 현재 파일
├── subagent-convention/       ← 오케스트레이션 스킬
│   └── _index.md
├── db-query/                  ← DB 쿼리 스킬
│   └── _index.md
├── git-convention/            ← Git 컨벤션 스킬
│   └── _index.md
├── sync-config/               ← 설정 동기화 스킬
│   └── skill.md
└── dooray/                    ← Dooray 스킬
    └── skill.md
```

## 스킬 목록

| 스킬 | 인덱스 | 관련 커맨드 | 설명 |
|------|--------|-------------|------|
| 오케스트레이션 | `subagent-convention/_index.md` | `/orchestration` | 5단계 작업 흐름, 위임 체계 |
| DB 쿼리 | `db-query/_index.md` | `/db:query`, `/db:convert` | DB 연결, 스키마, 쿼리 |
| Git 컨벤션 | `git-convention/_index.md` | `/git:*` | 커밋 메시지, 브랜치 규칙 |
| 설정 동기화 | `sync-config/skill.md` | `/config:*` | 설정 파일 동기화 |
| Dooray | `dooray/skill.md` | `/dooray:messenger` | Dooray 메신저 연동 |

## 스킬-커맨드 매핑

```
skills/subagent-convention/ ◄────── /orchestration
├── instruction.md
├── config.md
└── templates/*.md

skills/db-query/ ◄────────────────── /db:query, /db:convert
├── skill.md
├── databases.md
├── templates.md
└── schema/*.md

skills/git-convention/ ◄──────────── /git:save, /git:push, /git:switch
└── SKILL.md

skills/sync-config/ ◄────────────── /config:push, /config:sync
└── skill.md

skills/dooray/ ◄─────────────────── /dooray:messenger
└── skill.md
```

## 수정 가이드

### 스킬 내 파일 수정

```
1. 해당 스킬의 _index.md 읽기 (있으면)
2. 관련 커맨드 확인
3. 파일 수정
4. 관련 문서도 함께 수정 (필요시)
```

### 새 스킬 추가

```
1. skills/{skill-name}/ 폴더 생성
2. _index.md 생성 (메타 정보)
3. 스킬 파일 생성
4. 이 파일(_index.md)에 등록
5. 관련 커맨드가 있으면 커맨드 _index.md에도 참조 추가
```

### 스킬 삭제

```
1. 스킬 폴더 삭제
2. 이 파일(_index.md)에서 제거
3. 관련 커맨드의 참조도 제거
```

## 스킬별 상세

### 오케스트레이션 (`subagent-convention/`)

| 파일 | 용도 |
|------|------|
| `_index.md` | 문서 인덱스, 필수 확인 |
| `instruction.md` | 5단계 흐름, 역할 정의 |
| `config.md` | 모델 설정 |
| `templates/*.md` | 역할별 템플릿 |

### DB 쿼리 (`db-query/`)

| 파일 | 용도 |
|------|------|
| `_index.md` | 문서 인덱스 |
| `skill.md` | 쿼리 실행 가이드 |
| `databases.md` | DB 연결 정보 |
| `templates.md` | 쿼리 템플릿 |
| `schema/*.md` | 테이블 스키마 |

### Git 컨벤션 (`git-convention/`)

| 파일 | 용도 |
|------|------|
| `_index.md` | 문서 인덱스 |
| `SKILL.md` | 커밋/브랜치 규칙 |
