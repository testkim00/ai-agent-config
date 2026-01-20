# 커맨드 마스터 인덱스

> **커맨드 수정 시 필수 확인**
>
> 커맨드 파일 수정 전 반드시:
> 1. 해당 커맨드가 속한 그룹의 `_index.md` 확인
> 2. 관련 스킬이 있으면 스킬 문서도 확인
> 3. 일관성 있게 수정

## 커맨드 구조

```
commands/
├── _index.md              ← 현재 파일
├── codex.md               ← 단독 커맨드
├── consult.md             ← 단독 커맨드
├── fix-encoding.md        ← 단독 커맨드
├── orchestration.md       ← 단독 커맨드 (→ skills/subagent-convention/)
├── git/                   ← Git 그룹
│   ├── _index.md
│   ├── cleanup.md
│   ├── pr.md
│   ├── push.md
│   ├── save.md
│   ├── switch.md
│   └── sync.md
├── db/                    ← DB 그룹
│   ├── _index.md
│   ├── convert.md
│   └── query.md
├── project/               ← Project 그룹
│   ├── _index.md
│   ├── init-shared.md
│   ├── new.md
│   ├── push-shared.md
│   └── sync-shared.md
├── config/                ← Config 그룹
│   ├── _index.md
│   ├── push.md
│   └── sync.md
├── tidy/                  ← Tidy 그룹
│   ├── _index.md
│   ├── _common.md
│   └── md.md
└── dooray/                ← Dooray 그룹
    └── messenger.md
```

## 그룹별 인덱스

| 그룹 | 인덱스 | 커맨드 수 | 관련 스킬 |
|------|--------|-----------|-----------|
| [Git](#git-그룹) | `git/_index.md` | 6개 | `skills/git-convention/` |
| [DB](#db-그룹) | `db/_index.md` | 2개 | `skills/db-query/` |
| [Project](#project-그룹) | `project/_index.md` | 4개 | - |
| [Config](#config-그룹) | `config/_index.md` | 2개 | `skills/sync-config/` |
| [Tidy](#tidy-그룹) | `tidy/_index.md` | 2개 | - |

## 단독 커맨드

| 커맨드 | 파일 | 설명 | 관련 스킬 |
|--------|------|------|-----------|
| `/codex` | `codex.md` | Codex 호출 | - |
| `/consult` | `consult.md` | Codex 자문 | - |
| `/fix-encoding` | `fix-encoding.md` | 터미널 인코딩 수정 | - |
| `/orchestration` | `orchestration.md` | 오케스트레이션 실행 | `skills/subagent-convention/` |

## Git 그룹

| 커맨드 | 파일 | 설명 |
|--------|------|------|
| `/git:cleanup` | `cleanup.md` | 머지된 브랜치 정리 |
| `/git:pr` | `pr.md` | PR 생성 |
| `/git:push` | `push.md` | 커밋 후 푸시 |
| `/git:save` | `save.md` | 변경사항 스테이징/커밋 |
| `/git:switch` | `switch.md` | 브랜치 전환/생성 |
| `/git:sync` | `sync.md` | 원격 동기화 |

**관련 스킬:** `skills/git-convention/SKILL.md`

## DB 그룹

| 커맨드 | 파일 | 설명 |
|--------|------|------|
| `/db:query` | `query.md` | DB 쿼리 실행 |
| `/db:convert` | `convert.md` | 쿼리 결과 변환 |

**관련 스킬:** `skills/db-query/`

## Project 그룹

| 커맨드 | 파일 | 설명 |
|--------|------|------|
| `/project:new` | `new.md` | 새 프로젝트 생성 |
| `/project:init-shared` | `init-shared.md` | 공유 모듈 초기화 |
| `/project:sync-shared` | `sync-shared.md` | 공유 모듈 동기화 |
| `/project:push-shared` | `push-shared.md` | 공유 모듈 푸시 |

## Config 그룹

| 커맨드 | 파일 | 설명 |
|--------|------|------|
| `/config:push` | `push.md` | 설정 변경사항 푸시 |
| `/config:sync` | `sync.md` | 원격 설정 동기화 |

**관련 스킬:** `skills/sync-config/skill.md`

## Tidy 그룹

| 커맨드 | 파일 | 설명 |
|--------|------|------|
| `/tidy:md` | `md.md` | 마크다운 정리 |
| (공통) | `_common.md` | 공통 규칙 |

## 수정 가이드

### 그룹 내 커맨드 수정

```
1. 해당 그룹의 _index.md 읽기
2. 관련 스킬 확인 (있으면 스킬 문서도 읽기)
3. 커맨드 파일 수정
4. 필요 시 관련 문서도 수정
```

### 새 커맨드 추가

```
1. 커맨드 파일 생성
2. 해당 그룹의 _index.md에 등록
3. 이 파일(_index.md)에도 등록
4. 관련 스킬이 있으면 스킬 _index.md에도 참조 추가
```

### 커맨드 삭제

```
1. 커맨드 파일 삭제
2. 해당 그룹의 _index.md에서 제거
3. 이 파일(_index.md)에서도 제거
4. 관련 스킬의 참조도 제거
```
