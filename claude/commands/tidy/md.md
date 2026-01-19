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
3. **중복 제거** - 동일/유사 내용 병합, 반복 설명 통합
4. **구조 정리** - 논리적 순서 재배치, 관련 내용 그룹화
5. **결과 출력** - 변경 전/후 비교, 저장
6. **자동 동기화** - `~/.ai-agent-config`에 변경사항 반영

## 자동 동기화

정리 완료 후 `~/.claude/skills/sync-config/skill.md` 참조하여 동기화 처리.

- commands, skills: 심볼릭 링크 (자동 반영)
- CLAUDE.md: `sync_claude_md` 실행

## 정리 기준

- 제목 계층 정리 (h1 → h2 → h3 순서)
- 빈 줄 정규화 (연속 빈 줄 → 단일 빈 줄)
- 목록 스타일 통일
- 테이블 정렬
- 불필요한 공백 제거

## 주의사항

- 원본 의미 손실 방지
- 의도적 반복(강조)은 유지
- 불확실한 경우 사용자에게 확인

## 출력 예시

```
[대상] 3개 파일 발견
[분석] instruction.md (150줄)
[중복] 2개 항목 → 통합
[정리] 완료 (150줄 → 120줄, -20%)
[저장] instruction.md ✓

[요약] 3개 파일 처리, 총 45줄 감소
```
