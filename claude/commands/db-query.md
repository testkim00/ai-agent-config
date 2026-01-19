# DB Query 커맨드

데이터베이스에 자연어로 쿼리를 요청하고, 선택적으로 템플릿에 데이터를 채워 파일로 출력합니다.

## 사용법

### 기본 (콘솔 출력)
```
/db:query {자연어 요청}
/db:query {DB이름} {자연어 요청}
```

### 파일 출력 (> 사용)
```
/db:query {자연어 요청} > {템플릿파일}
/db:query {자연어 요청} > {템플릿파일} > {출력파일}
```

**기본값:**
- DB 이름 생략 시 `WERPBiz` 사용
- 출력파일 생략 시 템플릿과 동일한 형식으로 저장

## 경로 규칙

| 입력 형태 | 해석 |
|-----------|------|
| `file.xlsx` (파일명만) | 템플릿: `~/Projects/db-templates/file.xlsx` |
| | 출력: `~/Projects/db-outputs/file_{timestamp}.xlsx` |
| `./file.xlsx` (상대경로) | 현재 작업 디렉토리 기준 |
| `~/path/file.xlsx` (절대경로) | 지정된 경로 그대로 사용 |
| `/path/file.xlsx` (절대경로) | 지정된 경로 그대로 사용 |

## 예시

### 콘솔 출력
```
/db:query 재직중인 직원 목록 보여줘
/db:query WERPBiz 도급직원 최근 입사자
```

### 템플릿 적용 (기본 폴더)
```
/db:query 도급직원 입사자 > 직원목록.xlsx
```
→ 템플릿: `~/Projects/db-templates/직원목록.xlsx`
→ 출력: `~/Projects/db-outputs/직원목록_20260117.xlsx`

### 템플릿 → 다른 형식 변환
```
/db:query 월별 매출 현황 > 매출보고서.xlsx > 월간매출_202601.pdf
```
→ 출력: `~/Projects/db-outputs/월간매출_202601.pdf`

### 경로 직접 지정
```
/db:query 직원 명단 > ~/Documents/템플릿.xlsx > ./output/보고서.pdf
```

---

## 처리 흐름

### 스키마 확인 (우선순위)

1. `schema/_summary.md` (요약본)
2. `schema/{DB이름}.md` (상세)
3. `SELECT TOP 1 * FROM 테이블명` (컬럼 확인)

### 위임 판단

| 작업량 | 처리 |
|--------|------|
| 쿼리 1~2개 | 직접 실행 |
| 쿼리 3개+ | 병렬 위임 |

### 쿼리 실행

```bash
python3 ~/.claude/skills/db-query/query.py "ERP" "SELECT ..."
```

---

## 템플릿 작성 가이드

상세 내용은 `~/.claude/skills/db-query/templates.md` 참조

### 플레이스홀더 문법
```
{{column_name}}       - 단일 값 (첫 번째 행의 해당 컬럼)
{{#rows}}...{{/rows}} - 반복 영역 (모든 행에 대해 반복)
{{@today}}            - 현재 날짜 (YYYY-MM-DD)
{{@now}}              - 현재 시간 (YYYY-MM-DD HH:mm:ss)
{{@count}}            - 총 행 수
```

### 예시 (엑셀 템플릿)
```
A1: 직원 목록 ({{@today}} 기준, 총 {{@count}}명)
A3: 사번 | B3: 이름 | C3: 입사일
A4: {{#rows}}{{emp_id}} | {{emp_name}} | {{enter_date}}{{/rows}}
```

## 지원 형식

| 입력 (템플릿) | 출력 가능 형식 |
|--------------|---------------|
| .xlsx | .xlsx, .pdf, .csv |
| .docx | .docx, .pdf |
| .pptx | .pptx, .pdf |

## 파이프라인 (|)

여러 커맨드를 `|`로 연결하여 순차 실행할 수 있습니다.
앞 커맨드의 출력 파일이 다음 커맨드의 입력으로 자동 전달됩니다.

### 문법
```
/db:query {요청} > {템플릿} | /db:convert {형식} {출력파일}
/db:query {요청} > {템플릿} | /dooray:messenger {수신자}
```

### 예시

```bash
# 쿼리 → 엑셀 생성 → PDF 변환
/db:query 도급직원 입사자 > 직원목록.xlsx | /db:convert pdf 입사자현황.pdf

# 쿼리 → 엑셀 생성 → 메신저 전송
/db:query 최근 입사자 10명 > 입사자.xlsx | /dooray:messenger 김범수

# 3단 파이프라인
/db:query 월간현황 > 보고서.xlsx | /db:convert pdf | /dooray:messenger kbs
```

### 파이프라인 처리 규칙

| 순서 | 동작 |
|------|------|
| 1 | `\|` 기준으로 커맨드 분리 |
| 2 | 첫 번째 커맨드 실행 → 출력 파일 경로 저장 |
| 3 | 다음 커맨드에 `$PIPE_INPUT` 변수로 파일 경로 전달 |
| 4 | 마지막 커맨드까지 순차 실행 |

### 파이프 변수

| 변수 | 설명 |
|------|------|
| `$PIPE_INPUT` | 이전 커맨드의 출력 파일 경로 |
| `$PIPE_FILENAME` | 이전 출력 파일명 (확장자 제외) |
| `$PIPE_EXT` | 이전 출력 파일 확장자 |

### 주의사항

- 파이프라인은 파일 출력이 있는 커맨드에서만 사용 가능
- 콘솔 출력만 하는 경우 `| /dooray:messenger`로 텍스트 전달
- 에러 발생 시 파이프라인 중단, 에러 메시지 출력

## 후속 변환 (단독)

파일 출력 후 별도로 변환하려면:
```
/db:convert pdf      # 마지막 출력 → PDF
/db:convert csv      # 마지막 출력 → CSV
```
