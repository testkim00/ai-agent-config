# DB Convert 커맨드

파일을 다른 형식으로 변환합니다.

## 사용법

```
/db:convert {형식}
/db:convert {형식} {출력파일명}
```

## 입력 파일 결정

| 우선순위 | 조건 | 입력 파일 |
|---------|------|----------|
| 1 | 파이프라인 (`\|`) 으로 연결됨 | `$PIPE_INPUT` (이전 커맨드 출력) |
| 2 | 단독 실행 | 마지막 `/db:query` 출력 파일 |

## 지원 형식

| 형식 | 설명 |
|------|------|
| `pdf` | PDF 문서로 변환 |
| `csv` | CSV 파일로 변환 |
| `xlsx` | 엑셀 파일로 변환 |

## 파일명 규칙

| 명령 | 출력 파일명 |
|------|------------|
| `/db:convert pdf` | 마지막 파일명 기반 자동 생성 |
| `/db:convert pdf report.pdf` | 지정한 파일명 사용 |

## 예시

```
/db:convert pdf                    # → 도급직원입사자_20260117.pdf (자동)
/db:convert pdf 월간보고서.pdf      # → 월간보고서_20260117.pdf (지정)
/db:convert csv                    # → 도급직원입사자_20260117.csv (자동)
/db:convert csv 직원목록.csv        # → 직원목록_20260117.csv (지정)
```

---

## 처리 흐름 (Subagent 활용)

> 모델 설정: `~/.claude/skills/subagent-convention/config.md` 참조

### 역할 분담

| 역할 | 담당 | 작업 |
|------|------|------|
| **판단** | Opus (메인) | 입력 파일 결정, 변환 형식 확인 |
| **실행** | Sonnet subagent | 실제 파일 변환 작업 |

### Phase 1: 판단 (Opus)

1. 마지막 출력 파일 확인
2. 변환 형식 결정
3. 출력 경로 결정

마지막 출력 파일이 없으면:
> "변환할 파일이 없습니다. 먼저 `/db:query`를 실행해주세요."

### Phase 2: 변환 실행 (Sonnet Subagent)

**파일 변환 작업을 sonnet subagent에게 위임:**

```
Task(
    subagent_type="sonnet",
    model="sonnet",
    prompt="""
    파일 변환 작업:

    입력 파일: {입력 파일 경로}
    출력 형식: {형식}
    출력 경로: {출력 파일 경로}

    변환 방법:
    - xlsx → pdf: LibreOffice 사용
      soffice --headless --convert-to pdf --outdir {출력폴더} {입력파일}
    - xlsx → csv: pandas 사용
      df = pd.read_excel(입력); df.to_csv(출력, encoding='utf-8-sig')
    - csv → xlsx: pandas 사용
      df = pd.read_csv(입력); df.to_excel(출력, index=False)

    결과:
    - 변환 성공 시 출력 파일 경로 반환
    - 실패 시 에러 메시지 반환
    """
)
```

### Phase 3: 결과 확인 (Opus)

- 변환 결과 확인
- 사용자에게 결과 알림

---

## 형식별 변환 코드 (Sonnet 참고용)

### xlsx → pdf
```python
import subprocess
import os

input_file = "{입력파일}"
output_dir = os.path.dirname("{출력파일}")

subprocess.run([
    'soffice', '--headless', '--convert-to', 'pdf',
    '--outdir', output_dir,
    input_file
])
```

### xlsx → csv
```python
import pandas as pd

df = pd.read_excel("{입력파일}")
df.to_csv("{출력파일}", index=False, encoding='utf-8-sig')
```

### csv → xlsx
```python
import pandas as pd

df = pd.read_csv("{입력파일}")
df.to_excel("{출력파일}", index=False)
```

---

## 출력 경로

- 기본: `~/Projects/db-outputs/{원본파일명}.{새형식}`
- 파일명 지정 시: `~/Projects/db-outputs/{지정파일명}.{형식}`

## 변환 매트릭스

| 원본 | → pdf | → csv | → xlsx |
|------|-------|-------|--------|
| .xlsx | ✅ | ✅ | - |
| .csv | ✅ | - | ✅ |
| .docx | ✅ | ❌ | ❌ |

## 주의사항

- CSV 변환 시 서식 정보는 손실됩니다
- 한글 인코딩은 `utf-8-sig` 사용 (엑셀 호환)

## PDF 변환 요구사항

PDF 변환에는 LibreOffice가 필요합니다.

**설치 방법 (macOS):**
```bash
brew install --cask libreoffice
```

**설치 후 경로 확인:**
```bash
/Applications/LibreOffice.app/Contents/MacOS/soffice --version
```

**미설치 시 대안:**
- CSV로 변환 후 다른 도구로 PDF 생성
- 엑셀에서 직접 PDF 내보내기
