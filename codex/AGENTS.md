# Global Agent Notes

- When a task requires network access, immediately request user approval for network access; do not respond with a generic "network access not available" message.

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
