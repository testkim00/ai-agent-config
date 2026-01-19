# File Processor Template

파일 처리용 subagent 템플릿 (읽기, 쓰기, 변환)

## 템플릿

```python
Task(
    subagent_type="Bash",
    model="sonnet",  # config.md 참조
    prompt="""
    {작업명} 파일 처리:

    [입력 파일]: {input_path}
    [출력 파일]: {output_path}
    [처리 방식]: {process_type}

    [처리 단계]:
    1. 입력 파일 확인
       - 파일 존재 여부
       - 파일 형식 확인

    2. 데이터 처리
       - {processing_logic}

    3. 출력 파일 생성
       - {output_format}

    4. 결과 확인
       - 파일 생성 확인
       - 내용 검증

    [출력]:
    - 처리된 파일 경로
    - 처리 건수
    - 성공/실패 여부
    """
)
```

## 사용 예시

### Excel → PDF 변환

```python
Task(
    subagent_type="Bash",
    model="sonnet",
    prompt="""
    파일 변환 작업:

    [입력 파일]: {xlsx_path}
    [출력 형식]: PDF
    [출력 경로]: {output_dir}

    [처리 단계]:
    1. 입력 파일 확인
       - xlsx 파일 존재 확인

    2. 변환 실행
       - Python openpyxl로 읽기
       - reportlab으로 PDF 생성

    3. 결과 확인
       - PDF 파일 생성 확인

    [출력]:
    - 생성된 PDF 경로
    - 성공/실패 여부
    """
)
```

### JSON 파일 처리

```python
Task(
    subagent_type="Bash",
    model="sonnet",
    prompt="""
    JSON 데이터 처리:

    [입력 파일]: ~/data/employees.json
    [처리]: 부서별 집계

    [처리 단계]:
    1. JSON 파일 읽기
    2. 부서별 그룹화
    3. 집계 결과 생성

    [출력]:
    - 부서별 인원 수
    - 총 인원 수
    """
)
```
