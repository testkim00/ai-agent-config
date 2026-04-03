# Global Agent Notes

- When a task requires network access, request user approval only if the current environment or tool policy actually blocks network access; do not respond with a generic "network access not available" message.

## 환경변수 (.env)

`~/.codex/.env` 파일에 DB 접속정보와 API 토큰이 저장되어 있습니다.

**DB 접속정보:**
```
{PREFIX}_DB_TYPE=mssql|mysql|postgres
{PREFIX}_DB_HOST=호스트
{PREFIX}_DB_PORT=포트
{PREFIX}_DB_NAME=데이터베이스명
{PREFIX}_DB_USER=사용자
{PREFIX}_DB_PASSWORD=비밀번호
```

**API 토큰:**
```
{PREFIX}_API_TOKEN=토큰값
```

db-query 스킬 사용 시 이 파일의 PREFIX를 참조하세요.
예: `ERP`, `AZURE`, `DOORAY` 등

## Skills 참조

`~/.codex/skills/` 폴더에 있는 스킬들을 참조할 수 있습니다:
- db-query: DB 쿼리 관련 (`.env`의 DB 접속정보 사용)
- dooray: Dooray 메신저 연동 (`.env`의 DOORAY_API_TOKEN 사용)
- git-convention: Git 커밋/브랜치 컨벤션
- document-skills: 문서 작업 (pdf, xlsx, docx, pptx 등)
- frontend-design: 프론트엔드 UI 디자인

각 스킬의 SKILL.md 파일을 읽어서 사용법을 확인하세요.

## 관계 파일 (_relations.yaml)

- `~/.codex/_relations.yaml` 에 Codex skills, upstream Claude commands, 공용 문서, skill internals 관계가 정리되어 있습니다.
- 스킬이나 커맨드를 생성, 수정, 이름 변경, 삭제할 때는 `반드시` 먼저 이 파일에서 관련 항목을 찾고, 연결된 문서와 내부 파일을 `전부 검토한 뒤` 진행하세요.
- 스킬이나 커맨드를 생성, 이름 변경, 삭제할 때는 `반드시` `_relations.yaml`도 같은 변경에서 함께 업데이트하세요.
- 필수 순서:
  1. `_relations.yaml`에서 관계 항목 확인
  2. 연결된 skill/command 확인
  3. `skill_internals`에 적힌 내부 파일 확인
  4. 필요한 문서를 전부 읽은 뒤 수정
  5. 스킬 또는 커맨드 생성/삭제/이름 변경이면 `_relations.yaml` 갱신

## Repo Harness

- 이 저장소에는 repo 기본 harness 설정 파일인 `/Users/honeychaser/Projects/ai-agent-config/.codex/harness.json` 이 있습니다.
- `implementation`, `bugfix`, `refactor`, `ops` 성격의 turn을 끝낼 때는 이 파일의 검증 요구사항을 우선 따르세요.
- 이 규칙은 orchestration 스킬과 별개로 hook에서 강제됩니다.
- 검증이 정말 불가능하면 최종 메시지에 `HARNESS_SKIP: <reason>` 을 명시적으로 남기세요.
