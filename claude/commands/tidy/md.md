# Tidy MD

마크다운 파일의 중복을 제거하고 내용을 정리합니다.

## 사용법

```
/tidy:md              # 최근 수정/추가된 md 파일 정리
/tidy:md all          # ~/.claude 밑의 모든 md 파일 정리
/tidy:md skills       # skills 폴더만
/tidy:md commands     # commands 폴더만
/tidy:md plugins      # plugins 폴더만
/tidy:md {파일경로}   # 특정 파일 지정
```

## 대상 파일 결정

| 인자 | 대상 |
|------|------|
| (없음) | `~/.ai-agent-config`에서 최근 변경된 md 파일 (`git diff --name-only HEAD~1`) |
| `all` | `~/.claude/**/*.md` 전체 |
| `skills` | `~/.claude/skills/**/*.md` |
| `commands` | `~/.claude/commands/**/*.md` |
| `plugins` | `~/.claude/plugins/**/*.md` |
| 파일경로 | 지정된 파일 |

## 처리 흐름

1. **대상 파일 수집** - 인자에 따라 파일 목록 생성
2. **파일별 분석** - 구조 파악 (섹션, 목록, 테이블)
3. **중복 제거** - 동일한 내용이 반복되는 경우만 병합
4. **문구 다듬기** - 가독성 향상, 표현 정리 (내용 유지)
5. **포맷 정리** - 일관된 스타일로 보기 좋게 정돈
6. **결과 출력** - 변경 전/후 비교, 저장
7. **자동 동기화** - `~/.ai-agent-config`에 변경사항 반영

> ⚠️ **기존 내용 생략/축소 금지** - 정보량은 유지하면서 보기 좋게 정리

## 자동 동기화

정리 완료 후 `~/.claude/skills/sync-config/skill.md` 참조하여 동기화 처리.

- commands, skills: 심볼릭 링크 (자동 반영)
- CLAUDE.md: `sync_claude_md` 실행

## 주의사항

> **[_common.md](./_common.md) 참조** - 모든 tidy 명령어 공통 규칙 적용

### MD 파일 정리 기준

- 제목 계층 (h1 → h2 → h3)
- 빈 줄 정규화
- 목록/테이블 스타일 통일
- 불필요한 공백 제거
