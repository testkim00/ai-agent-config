# Project 커맨드 인덱스

> **수정 시 필수 확인**
>
> Project 커맨드 수정 전:
> 1. 이 파일의 관련 문서 목록 확인
> 2. 공유 모듈 구조 (ui-shell, components, core) 이해

## 문서 구조

```
commands/project/
├── _index.md           ← 현재 파일
├── new.md              ← 새 프로젝트 생성
├── init-shared.md      ← 공유 모듈 초기화
├── sync-shared.md      ← 공유 모듈 동기화
└── push-shared.md      ← 공유 모듈 푸시
```

## 커맨드 목록

| 커맨드 | 파일 | 설명 |
|--------|------|------|
| `/project:new` | `new.md` | 새 프로젝트 생성 |
| `/project:init-shared` | `init-shared.md` | 공유 모듈 초기화 (subtree 설정) |
| `/project:sync-shared` | `sync-shared.md` | 공유 모듈 최신화 (pull) |
| `/project:push-shared` | `push-shared.md` | 공유 모듈 변경 푸시 |

## 공유 모듈 구조

```
_shared/
├── ui-shell/       ← testkim00/ui-shell
├── components/     ← testkim00/ui-components
└── core/           ← testkim00/core-lib
```

## 워크플로우

```
새 프로젝트
    │
    ▼
/project:new (프로젝트 생성)
    │
    ▼
/project:init-shared (공유 모듈 추가)
    │
    ▼
... 개발 ...
    │
    ├─► 공유 모듈 업데이트 필요
    │       │
    │       ▼
    │   /project:sync-shared
    │
    └─► 공유 모듈 변경 완료
            │
            ▼
        /project:push-shared
```

## 수정 시 체크리스트

- [ ] 공유 모듈 경로 변경 → 모든 커맨드 함께 수정
- [ ] 새 공유 모듈 추가 → `init-shared.md`, `sync-shared.md`, `push-shared.md` 수정
- [ ] 프로젝트 템플릿 변경 → `new.md` 수정
