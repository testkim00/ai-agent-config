# DB Query Skill

자연어로 데이터베이스 쿼리를 요청받아 실행하고, 선택적으로 템플릿에 결과를 채워 파일로 출력합니다.

## 파일 구조

```
~/.claude/
├── .env                          # DB 연결 정보 (보안)
├── commands/
│   └── db:query.md               # 커맨드 진입점
└── skills/
    └── db-query/
        ├── skill.md              # 이 파일 (실행 가이드)
        ├── databases.md          # DB 이름 → 접두어 매핑
        ├── templates.md          # 템플릿 작성 가이드
        ├── schema/
        │   └── {DB이름}.md       # 테이블/컬럼 설명
        └── query.py              # 쿼리 실행 스크립트

~/Projects/
├── db-templates/                 # 템플릿 파일 저장
└── db-outputs/                   # 출력 파일 저장
```

## 명령어 문법

### 기본 (콘솔 출력)
```
/db:query {자연어 요청}
/db:query {DB이름} {자연어 요청}
```

### 파일 출력 (`>` 사용)
```
/db:query {자연어 요청} > {템플릿파일}
/db:query {자연어 요청} > {템플릿파일} > {출력파일}
```

### 후속 변환 (체이닝)
```
/db:convert {형식}
/db:convert {형식} {출력파일명}
```

## 경로 규칙

| 입력 형태 | 해석 |
|-----------|------|
| `file.xlsx` (파일명만) | 템플릿: `~/Projects/db-templates/` |
| | 출력: `~/Projects/db-outputs/` |
| `./file.xlsx` (상대경로) | 현재 작업 디렉토리 기준 |
| `~/path/file.xlsx` | 절대경로 그대로 사용 |
| `/path/file.xlsx` | 절대경로 그대로 사용 |

## 파일 출력 처리 규칙

### 템플릿 파일이 존재하는 경우
```
/db:query 쿼리 > 직원목록.xlsx
```
1. `~/Projects/db-templates/직원목록.xlsx` 존재 확인 ✓
2. **템플릿 복사** (원본 절대 수정 안 함)
3. 복사본에 쿼리 결과 삽입 (플레이스홀더 치환)
4. `~/Projects/db-outputs/직원목록_20260117.xlsx`로 저장

### 템플릿 파일이 없는 경우
```
/db:query 쿼리 > 신규보고서.xlsx
```
1. `~/Projects/db-templates/신규보고서.xlsx` 존재 확인 ✗
2. **새 엑셀 파일 생성** (기본 테이블 형식)
3. 쿼리 결과 직접 삽입 (헤더 + 데이터)
4. `~/Projects/db-outputs/신규보고서_20260117.xlsx`로 저장

### 출력 파일명 규칙
- 기본 형식: `{파일명}_{yyyyMMdd}.{확장자}`
- 예: `직원목록_20260117.xlsx`, `매출보고서_20260117.pdf`

**중요: 원본 템플릿 파일은 절대 수정하지 않음**

---

## 중요: 구현 시 주의사항

### DB 연결은 반드시 query.py 사용

**절대 직접 pymssql/pymysql 연결하지 말 것!**

```python
# ❌ 잘못된 방법 - 연결 실패함
import pymssql
conn = pymssql.connect(server=..., user=..., password=...)

# ✅ 올바른 방법 - query.py 사용
import subprocess
result = subprocess.run([
    'python3', '~/.claude/skills/db-query/query.py',
    'ERP', 'SELECT * FROM table'
], capture_output=True, text=True)
```

**이유**: query.py는 .env 파싱, TDS 버전, 타임아웃 등 검증된 연결 설정 포함

### 엑셀/문서 처리는 Python 라이브러리 직접 사용

**document-skills는 openpyxl/pandas 사용 가이드**일 뿐, 별도 자동화 도구 아님.
실제 처리는 Python 라이브러리 직접 사용:

| 파일 형식 | 사용할 라이브러리 |
|-----------|------------------|
| .xlsx | `openpyxl` (데이터 분석은 `pandas`) |
| .docx | `python-docx` |
| .pdf | `reportlab`, `PyPDF2` |

```python
# 엑셀 처리 예시
from openpyxl import load_workbook
wb = load_workbook('template.xlsx')
ws = wb.active
ws['A1'] = '데이터'
wb.save('output.xlsx')
```

#### document-skills에서 유용한 것
- `recalc.py`: 수식 재계산 스크립트 (LibreOffice 사용)
  ```bash
  python ~/.claude/plugins/cache/anthropic-agent-skills/document-skills/*/skills/xlsx/recalc.py output.xlsx
  ```
- 금융 모델 색상 코딩 표준 (필요시 참고)

---

## 처리 흐름

### Phase 1: 명령어 파싱

1. **파이프(`|`) 확인**
   - 없음 → 콘솔 출력 모드
   - 있음 → 템플릿 모드

2. **리다이렉트(`>`) 확인**
   - 없음 → 템플릿과 동일 형식 출력
   - 있음 → 지정된 형식으로 변환

3. **경로 해석**
   - 파일명만 → 기본 경로 사용
   - 절대/상대경로 → 해당 경로 사용

### Phase 2: 쿼리 실행

1. `databases.md`에서 DB 이름 → 접두어 매핑 확인
2. `schema/{DB이름}.md`에서 테이블/컬럼 정보 확인
3. 자연어 요청을 SQL 쿼리로 변환
4. `query.py`로 쿼리 실행

```bash
python3 ~/.claude/skills/db-query/query.py "{접두어}" "{SQL쿼리}"
```

### Phase 3: 결과 출력

#### 콘솔 모드
- 테이블 형식으로 콘솔에 출력

#### 템플릿 모드
1. **템플릿 읽기**: document-skills 활용
2. **플레이스홀더 치환**: 쿼리 결과 매핑
3. **파일 저장**: 출력 경로에 저장
4. **형식 변환**: 필요시 PDF 등으로 변환

---

## 템플릿 모드 상세

### 템플릿 경로 해석

| 입력 | 해석 결과 |
|------|----------|
| `employee.xlsx` | `~/Projects/db-templates/employee.xlsx` |
| `./my-template.xlsx` | 현재 작업 디렉토리 기준 |
| `~/Documents/t.xlsx` | 절대 경로 |

### 출력 경로 해석

| 입력 | 해석 결과 |
|------|----------|
| 생략 | `~/Projects/db-outputs/{템플릿명}_{timestamp}.{확장자}` |
| `report.pdf` | `~/Projects/db-outputs/report.pdf` |
| `./output.xlsx` | 현재 작업 디렉토리 기준 |

### 실제 구현 방법

**document-skills는 참고 가이드**이며, 실제 처리는 Python 라이브러리 직접 사용:

| 파일 형식 | Python 라이브러리 | 참고 스킬 |
|-----------|------------------|-----------|
| .xlsx | `openpyxl` | document-skills:xlsx |
| .docx | `python-docx` | document-skills:docx |
| .pptx | `python-pptx` | document-skills:pptx |
| .pdf | `reportlab` | document-skills:pdf |

#### 처리 순서

1. **쿼리 실행**: query.py로 데이터 조회
2. **결과 파싱**: 텍스트 출력을 파싱하여 리스트/딕셔너리로 변환
3. **템플릿 읽기**: openpyxl 등으로 템플릿 파일 로드
4. **플레이스홀더 치환**: 셀/텍스트에 데이터 삽입
5. **파일 저장**: 출력 경로에 저장

---

## 플레이스홀더 문법

### 데이터 바인딩
```
{{column_name}}       # 단일 값 (첫 번째 행)
{{#rows}}...{{/rows}} # 반복 영역
```

### 시스템 변수
```
{{@today}}   # 현재 날짜 (YYYY-MM-DD)
{{@now}}     # 현재 시간 (YYYY-MM-DD HH:mm:ss)
{{@count}}   # 총 행 수
```

---

## 지원 DB 타입

| 타입 | 라이브러리 | SQL 문법 |
|------|-----------|----------|
| mssql | pymssql | TOP N, GETDATE() |
| mysql | pymysql | LIMIT N, NOW() |
| postgres | psycopg2 | LIMIT N, NOW() |

---

## 보안 주의사항

1. **SELECT 전용**: INSERT/UPDATE/DELETE는 사용자 확인 후 실행
2. **민감 데이터**: 주민번호, 비밀번호 등 조회 시 주의
3. **대용량 방지**: 항상 LIMIT/TOP 사용 권장
4. **출력 파일**: 민감 데이터 포함 시 사용자에게 알림

---

## 유틸리티 명령

```bash
# 등록된 DB 목록 확인
python3 ~/.claude/skills/db-query/query.py --list
```

---

## 예시 시나리오

### 1. 기본 콘솔 출력
```
사용자: /db:query 도급직원 최근 입사자 10명

→ SQL 생성: SELECT TOP 10 * FROM hrdEmpMaster ORDER BY enter_date DESC
→ query.py 실행
→ 콘솔에 테이블 출력
```

### 2. 템플릿으로 엑셀 출력
```
사용자: /db:query 도급직원 입사자 | employee-list.xlsx

→ SQL 생성 및 실행
→ document-skills:xlsx 스킬 활용
→ ~/Projects/db-templates/employee-list.xlsx 읽기
→ 플레이스홀더 치환
→ ~/Projects/db-outputs/employee-list_20260117_143052.xlsx 저장
```

### 3. 템플릿에서 PDF로 변환
```
사용자: /db:query 월간 매출 | sales-report.xlsx > sales-202601.pdf

→ SQL 생성 및 실행
→ document-skills:xlsx로 템플릿 처리
→ document-skills:pdf로 PDF 변환
→ ~/Projects/db-outputs/sales-202601.pdf 저장
```
