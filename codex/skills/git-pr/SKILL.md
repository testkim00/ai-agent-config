---
name: git-pr
description: 현재 작업 브랜치에서 Pull Request를 만들 때 사용한다. Claude의 `/git:pr` 대응 스킬이다. 브랜치 상태를 확인하고, main/master에서 실행을 막고, 변경 요약과 함께 push 후 PR을 생성해야 할 때 사용한다.
---

# Git PR

## 언제 사용하나

- 현재 브랜치 변경으로 PR을 만들 때
- PR 제목과 본문을 커밋/변경 내역 기준으로 정리해야 할 때

## source mapping

- Claude command: `/git:pr`

## 기본 규칙

- 현재 브랜치가 `main` 또는 `master`면 중단한다.
- 비교 기준 브랜치는 우선 현재 저장소의 기본 브랜치, 없으면 `main`, 그다음 `master` 순으로 판단한다.
- 커밋이 없거나 diff가 없으면 중단한다.
- `git-convention`이 있으면 제목 규칙을 따른다.
- push 없이 PR만 가정하지 않는다. 원격 브랜치가 없으면 먼저 push한다.

## 실행 절차

1. 현재 브랜치와 기본 브랜치 대비 `git log`/`git diff --stat`를 확인한다.
2. PR 생성 가능 여부를 판단한다.
3. 필요하면 이슈 연결 여부를 짧게 묻는다.
4. 커밋과 diff 기준으로 PR 제목과 본문 초안을 만든다.
5. 원격에 브랜치를 push한다.
6. 가능한 도구로 PR을 생성한다.
   - GitHub app 또는 `gh`가 있으면 사용
7. 생성 결과 URL을 반환한다.

## 사용자에게 물어봐야 하는 경우

- Issue를 새로 만들지, 기존 Issue를 연결할지 불분명할 때
- 기본 브랜치가 `main`/`master` 외 다른 이름으로 보이는데 자동 판정이 애매할 때

## 하지 말아야 할 것

- `main`/`master`에서 바로 PR을 만들지 않는다.
- force push를 전제하지 않는다.
- PR 본문을 커밋 내용과 무관한 일반론으로 채우지 않는다.

