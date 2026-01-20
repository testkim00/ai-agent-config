# Git 커맨드 인덱스

> **수정 시 필수 확인**
>
> Git 커맨드 수정 전:
> 1. 이 파일의 관련 문서 목록 확인
> 2. `skills/git-convention/SKILL.md` 확인
> 3. 커밋 메시지/브랜치 컨벤션과 일관성 유지

## 문서 구조

```
commands/git/
├── _index.md       ← 현재 파일
├── cleanup.md      ← 브랜치 정리
├── pr.md           ← PR 생성
├── push.md         ← 커밋 후 푸시
├── save.md         ← 스테이징/커밋
├── switch.md       ← 브랜치 전환
└── sync.md         ← 원격 동기화
```

## 커맨드 목록

| 커맨드 | 파일 | 설명 | 의존성 |
|--------|------|------|--------|
| `/git:save` | `save.md` | 변경사항 스테이징/커밋 | 컨벤션 |
| `/git:push` | `push.md` | 커밋 후 원격 푸시 | save |
| `/git:pr` | `pr.md` | Pull Request 생성 | push |
| `/git:sync` | `sync.md` | 원격과 동기화 (pull+rebase) | - |
| `/git:switch` | `switch.md` | 브랜치 생성/전환 | 컨벤션 |
| `/git:cleanup` | `cleanup.md` | 머지된 브랜치 정리 | - |

## 관련 스킬

| 스킬 | 경로 | 역할 |
|------|------|------|
| Git 컨벤션 | `skills/git-convention/SKILL.md` | 커밋 메시지, 브랜치명 규칙 |

## 워크플로우

```
작업 시작
    │
    ▼
/git:switch (브랜치 생성)
    │
    ▼
... 작업 ...
    │
    ▼
/git:save (커밋)
    │
    ▼
/git:push (푸시)
    │
    ▼
/git:pr (PR 생성)
    │
    ▼
머지 후
    │
    ▼
/git:cleanup (브랜치 정리)
```

## 수정 시 체크리스트

- [ ] 커밋 메시지 형식 변경 → `SKILL.md`, `save.md`, `push.md` 함께 수정
- [ ] 브랜치명 규칙 변경 → `SKILL.md`, `switch.md` 함께 수정
- [ ] PR 템플릿 변경 → `pr.md` 수정
- [ ] 새 커맨드 추가 → 이 파일, `commands/_index.md` 업데이트
