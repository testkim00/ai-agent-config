# Claude 설정 마스터 인덱스

> **문서 수정 시 필수 확인**
>
> MD 파일, 스킬, 커맨드 수정 전 반드시:
> 1. 이 파일에서 관련 그룹의 `_index.md` 확인
> 2. 해당 그룹의 `_index.md` 읽기
> 3. 관련 문서 목록 파악 후 일관성 있게 수정

## 디렉토리 구조

```
~/.claude/
├── _index.md              ← 현재 파일 (마스터 인덱스)
├── CLAUDE.md              ← 전역 설정 (모든 프로젝트 공통)
├── commands/              ← 슬래시 커맨드
│   ├── _index.md          ← 커맨드 마스터 인덱스
│   ├── git/               ← Git 관련 커맨드 그룹
│   │   └── _index.md
│   ├── db/                ← DB 관련 커맨드 그룹
│   │   └── _index.md
│   ├── project/           ← 프로젝트 관련 커맨드 그룹
│   │   └── _index.md
│   ├── config/            ← 설정 관련 커맨드 그룹
│   │   └── _index.md
│   └── tidy/              ← 정리 관련 커맨드 그룹
│       └── _index.md
└── skills/                ← 스킬 (지식/템플릿)
    ├── _index.md          ← 스킬 마스터 인덱스
    ├── subagent-convention/
    │   └── _index.md      ← 오케스트레이션 문서 인덱스
    ├── db-query/
    │   └── _index.md      ← DB 쿼리 스킬 인덱스
    └── ...
```

## 그룹별 메타 인덱스

| 그룹 | 인덱스 경로 | 설명 |
|------|-------------|------|
| **커맨드** | `commands/_index.md` | 모든 슬래시 커맨드 |
| **스킬** | `skills/_index.md` | 모든 스킬 |

### 커맨드 그룹

| 그룹 | 인덱스 경로 | 관련 스킬 |
|------|-------------|-----------|
| Git | `commands/git/_index.md` | `skills/git-convention/` |
| DB | `commands/db/_index.md` | `skills/db-query/` |
| Project | `commands/project/_index.md` | - |
| Config | `commands/config/_index.md` | `skills/sync-config/` |
| Tidy | `commands/tidy/_index.md` | - |

### 스킬 그룹

| 그룹 | 인덱스 경로 | 관련 커맨드 |
|------|-------------|-------------|
| 오케스트레이션 | `skills/subagent-convention/_index.md` | `/orchestration` |
| DB 쿼리 | `skills/db-query/_index.md` | `/db:query`, `/db:convert` |
| Git 컨벤션 | `skills/git-convention/_index.md` | `/git:*` |
| 동기화 | `skills/sync-config/_index.md` | `/config:*` |

## 수정 워크플로우

### 1. 단일 파일 수정

```
1. 수정할 파일이 속한 그룹 확인
2. 해당 그룹의 _index.md 읽기
3. 관련 문서 목록 확인
4. 필요 시 관련 문서도 함께 수정
5. _index.md 업데이트 (문서 추가/삭제 시)
```

### 2. 새 커맨드/스킬 추가

```
1. 파일 생성
2. 해당 그룹의 _index.md에 등록
3. 관련 스킬/커맨드가 있으면 상호 참조 추가
4. commands/_index.md 또는 skills/_index.md 업데이트
```

### 3. 커맨드/스킬 삭제

```
1. 파일 삭제
2. 해당 그룹의 _index.md에서 제거
3. 관련 문서의 참조도 제거
4. commands/_index.md 또는 skills/_index.md 업데이트
```

## 커맨드-스킬 연관 관계

```
/orchestration ──────────► skills/subagent-convention/
                           ├── instruction.md
                           ├── config.md
                           └── templates/*.md

/db:query ───────────────► skills/db-query/
/db:convert                ├── skill.md
                           ├── databases.md
                           ├── templates.md
                           └── schema/*.md

/git:* ──────────────────► skills/git-convention/
                           └── SKILL.md

/config:push ────────────► skills/sync-config/
/config:sync               └── skill.md

/codex ──────────────────► (단독)
/consult ────────────────► (단독)
```

## 주의사항

- `_index.md` 파일은 메타정보 용도로만 사용
- 실제 로직/지시사항은 개별 파일에 작성
- 그룹 간 의존성이 있으면 양쪽 `_index.md`에 명시
- 변경 후 `git status`로 누락된 파일 확인
