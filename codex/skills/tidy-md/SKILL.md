---
name: tidy-md
description: Claude command `/tidy:md` 대응 스킬. Claude의 `/tidy:md` 명령을 Codex에서 skill로 사용할 때 대응 매핑으로 사용한다.
---

# Tidy MD

## 언제 사용하나

- Claude command `/tidy:md` 대응 스킬.
- Claude의 `/tidy:md`를 Codex에서 같은 의도로 수행해야 할 때

## source mapping

- Claude command: `/tidy:md`
- Source file: `claude/commands/tidy/md.md`

## 기본 규칙

- source command의 의도를 유지한다.
- Claude 전용 구문인 `allowed-tools`, `Task`, `AskUserQuestion`은 Codex 실행 환경에 맞게 해석한다.
- 사용자가 같은 동작을 요청하면 아래 source workflow를 기준으로 수행한다.

## source workflow

# Tidy MD

마크다운 파일의 중복을 제거하고 내용을 정리합니다.

## 사용법

```
/tidy:md              # 최근 수정/추가된 md 파일 정리
/tidy:md all          # 현재 ai-agent-config repo의 모든 md 파일 정리
/tidy:md skills       # skills 폴더만
/tidy:md commands     # commands 폴더만
/tidy:md plugins      # plugin 관련 md만 (현재 repo에 있을 때)
/tidy:md {파일경로}   # 특정 파일 지정
```

## 대상 파일 결정

| 인자 | 대상 |
|------|------|
| (없음) | 현재 repo에서 최근 변경되거나 새로 추가된 md 파일 (`git status --short`, `git diff --name-only -- '*.md'`) |
| `all` | `ai-agent-config/claude/**/*.md`, `ai-agent-config/codex/**/*.md` 전체 |
| `skills` | `ai-agent-config/codex/skills/**/*.md` |
| `commands` | `ai-agent-config/claude/commands/**/*.md` |
| `plugins` | plugin 관련 md (현재 repo 구조에 plugin bundle 문서가 있을 때만) |
| 파일경로 | 지정된 파일 |

## 처리 흐름

1. **대상 파일 수집** - 인자에 따라 파일 목록 생성
2. **파일별 분석** - 구조 파악 (섹션, 목록, 테이블)
3. **중복 제거** - 동일한 내용이 반복되는 경우만 병합
4. **문구 다듬기** - 가독성 향상, 표현 정리 (내용 유지)
5. **포맷 정리** - 일관된 스타일로 보기 좋게 정돈
6. **결과 출력** - 변경 전/후 비교, 저장
7. **저장 및 반영** - source tree 기준으로 저장하고, symlink 환경이면 자동 반영 여부만 확인

> ⚠️ **기존 내용 생략/축소 금지** - 정보량은 유지하면서 보기 좋게 정리

## 저장/반영 원칙

정리 작업은 `ai-agent-config` 저장소의 source 파일을 직접 다듬는 것을 우선한다.

- source tree가 홈 디렉터리 설치 경로와 심볼릭 링크로 연결돼 있으면 추가 동기화 없이 반영된다.
- 별도 복제본을 운영 중일 때만 `config-sync` 또는 사용자 지정 sync 절차를 검토한다.
- 문서 정리 자체를 이유로 불필요한 자동 커밋이나 별도 sync 명령을 기본 실행하지 않는다.

## 주의사항

> Codex 쪽 공통 tidy helper는 아직 별도 파일로 분리돼 있지 않다. 필요하면 source helper인 `/Users/honeychaser/Projects/ai-agent-config/claude/commands/tidy/_common.md`를 참고한다.

### MD 파일 정리 기준

- 제목 계층 (h1 → h2 → h3)
- 빈 줄 정규화
- 목록/테이블 스타일 통일
- 불필요한 공백 제거
