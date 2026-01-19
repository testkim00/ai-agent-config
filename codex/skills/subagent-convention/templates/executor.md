# Executor Template

명령 실행용 subagent 템플릿 (git, shell 등)

## 템플릿

```python
Task(
    subagent_type="Bash",
    model="sonnet",  # config.md 참조
    prompt="""
    {작업명} 실행:

    [실행할 명령]:
    - {command1}
    - {command2}

    [처리 단계]:
    1. 사전 조건 확인
       - {precondition}

    2. 명령 실행
       - {main_command}

    3. 결과 확인
       - {verification}

    [출력]:
    - 성공/실패 여부
    - 실행 결과 요약
    - 오류 시 에러 메시지
    """
)
```

## 사용 예시

### Git 커밋

```python
Task(
    subagent_type="Bash",
    model="sonnet",
    prompt="""
    Git 커밋 작업:

    [변경사항]: {staged_files}

    [처리 단계]:
    1. 변경사항 상세 확인
       - git diff --staged

    2. 커밋 메시지 생성
       - conventional commit 형식
       - 한국어로 작성

    3. 커밋 실행
       - git commit -m "{message}"

    4. 결과 확인
       - git log -1

    [출력]:
    - 커밋 해시
    - 커밋 메시지
    """
)
```

### Shell 명령

```python
Task(
    subagent_type="Bash",
    model="sonnet",
    prompt="""
    빌드 실행:

    [처리 단계]:
    1. 의존성 설치
       - npm install

    2. 빌드 실행
       - npm run build

    3. 결과 확인
       - 빌드 산출물 확인

    [출력]:
    - 빌드 성공/실패
    - 에러 시 에러 내용
    """
)
```
