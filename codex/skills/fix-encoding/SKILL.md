---
name: fix-encoding
description: Claude command `/fix-encoding` 대응 스킬. Claude의 `/fix-encoding` 명령을 Codex에서 skill로 사용할 때 대응 매핑으로 사용한다.
---

# Fix Encoding

## 언제 사용하나

- Claude command `/fix-encoding` 대응 스킬.
- Claude의 `/fix-encoding`를 Codex에서 같은 의도로 수행해야 할 때

## source mapping

- Claude command: `/fix-encoding`
- Source file: `claude/commands/fix-encoding.md`

## 기본 규칙

- source command의 의도를 유지한다.
- Claude 전용 구문인 `allowed-tools`, `Task`, `AskUserQuestion`은 Codex 실행 환경에 맞게 해석한다.
- 사용자가 같은 동작을 요청하면 아래 source workflow를 기준으로 수행한다.

## source workflow

# 터미널 한글 인코딩 설정

Windows 터미널(PowerShell, Git Bash)에서 한글이 깨지지 않도록 환경을 설정합니다.

## 실행할 작업

### 1. 현재 설정 확인

```powershell
# PowerShell 인코딩 확인
[Console]::OutputEncoding.EncodingName

# Git 설정 확인
git config --global --list | findstr "encoding autocrlf quotepath"
```

### 2. PowerShell UTF-8 설정

PowerShell 프로필에 UTF-8 인코딩 설정을 추가합니다.

```powershell
# 프로필 파일 경로
$PROFILE

# 프로필 파일 생성 (없으면)
if (!(Test-Path -Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}
```

프로필에 추가할 내용:
```powershell
# UTF-8 인코딩 설정
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
$OutputEncoding = [System.Text.Encoding]::UTF8

# Git 출력 인코딩
$env:LESSCHARSET = 'utf-8'
```

### 3. Git 전역 설정

```bash
# 한글 경로 정상 표시 (필수)
git config --global core.quotepath false

# 커밋 메시지 인코딩
git config --global i18n.commitencoding utf-8
git config --global i18n.logoutputencoding utf-8

# 줄바꿈 자동 변환 비활성화 (Windows)
git config --global core.autocrlf false
```

### 4. 설정 확인 테스트

```powershell
# 한글 출력 테스트
Write-Host "한글 테스트: 안녕하세요"

# Git 상태 확인 (한글 파일명 정상 표시 확인)
git status
```

## 결과 보고 형식

```
**터미널 인코딩 설정 완료**

| 항목 | 설정값 |
|------|--------|
| PowerShell OutputEncoding | UTF-8 |
| Git core.quotepath | false |
| Git i18n.commitencoding | utf-8 |
| Git core.autocrlf | false |
```

## 문제 해결

### PowerShell 스크립트 실행 오류 시
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 설정 후에도 한글 깨짐
1. PowerShell 완전히 종료 후 재시작
2. Windows Terminal 사용 권장
3. 폰트: Consolas, D2Coding, 나눔고딕코딩 등 사용
