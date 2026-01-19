# 데이터베이스 목록

DB 이름과 .env 접두어 매핑 정보입니다.

## 기본 DB

**DB 이름을 생략하면 `WERPBiz`를 기본값으로 사용합니다.**

## 등록된 데이터베이스

| DB 이름 | .env 접두어 | 타입 | 설명 |
|---------|------------|------|------|
| WERPBiz | ERP | mssql | ERP 시스템 (인사, 급여, 회계 등) |

## 매핑 규칙

- 사용자가 `WERPBiz`라고 하면 → `.env`의 `ERP_DB_*` 환경변수 사용
- DB 이름은 대소문자 구분 없이 매칭

## 연결 정보 위치

실제 연결 정보(호스트, 포트, 계정 등)는 `~/.claude/.env` 파일에 저장되어 있습니다.

```
ERP_DB_TYPE=mssql
ERP_DB_HOST=xxx.xxx.xxx.xxx
ERP_DB_PORT=1433
ERP_DB_NAME=WERPBiz
ERP_DB_USER=xxx
ERP_DB_PASSWORD=xxx
ERP_DB_OPTIONS=tds_version=7.0
```

## 새 DB 추가 방법

1. `~/.claude/.env`에 연결 정보 추가 (새 접두어 사용)
2. 이 파일의 테이블에 매핑 추가
3. `schema/{DB이름}.md` 파일 생성
