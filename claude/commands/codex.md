# Codex 커맨드

OpenAI Codex CLI를 통해 질문하거나 작업을 위임합니다.

## 사용법

### 기본 (질문/작업 요청)
```
/codex {질문 또는 작업 요청}
```

### 네트워크 필요 시 (웹 검색, API 호출 등)
```
/codex --net {질문 또는 작업 요청}
/codex -n {질문 또는 작업 요청}
```

### 특정 모델 지정
```
/codex --model {모델명} {질문 또는 작업 요청}
/codex -m o3 {질문 또는 작업 요청}
```

## 옵션

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--net` | `-n` | 네트워크 접근 허용 (외부 API, 웹 검색 필요 시) |
| `--model` | `-m` | 사용할 모델 지정 (기본: gpt-5.2-codex) |
| `--auto` | `-a` | 완전 자동 모드 (승인 없이 실행) |

## 예시

### 기본 질문
```
/codex 이 프로젝트의 구조를 분석해줘
/codex Python에서 비동기 처리 방법 설명해줘
```

### 네트워크 필요한 작업
```
/codex --net 현재 원달러 환율 조회해줘
/codex -n 최신 React 문서에서 useEffect 사용법 찾아줘
/codex --net GitHub API로 이슈 목록 가져와줘
```

### 코드 작업 위임
```
/codex 이 함수를 리팩토링해줘
/codex 테스트 코드 작성해줘
/codex -a 모든 TODO 주석을 찾아서 정리해줘
```

## 처리 흐름

이 커맨드가 호출되면 다음과 같이 처리:

### 1. 옵션 파싱
- `--net` / `-n` 확인 → 네트워크 모드 결정
- `--model` / `-m` 확인 → 모델 지정
- `--auto` / `-a` 확인 → 자동 실행 모드

### 2. Codex CLI 실행

#### 기본 모드 (네트워크 제한)
```bash
codex exec "{프롬프트}" --full-auto
```

#### 네트워크 모드 (외부 접근 허용)
```bash
codex exec "{프롬프트}" --sandbox danger-full-access
```

#### 모델 지정
```bash
codex exec "{프롬프트}" --model {모델명} --full-auto
```

### 3. 결과 반환
- Codex의 응답을 파싱하여 사용자에게 전달
- 에러 발생 시 에러 메시지와 해결 방법 안내

## Claude 자동 사용 가이드라인

Claude는 다음 상황에서 Codex를 자동으로 활용할 수 있습니다:

### Codex에게 위임하면 좋은 작업
1. **대규모 코드 리팩토링** - 여러 파일에 걸친 대규모 변경
2. **복잡한 코드 생성** - 보일러플레이트가 많은 코드
3. **특정 프레임워크 전문 지식** - React, Vue, Django 등 최신 패턴
4. **실시간 정보 조회** (--net 필요) - 환율, 날씨, 최신 뉴스 등
5. **외부 API 호출** (--net 필요) - GitHub, Slack 등 API 연동

### Codex 사용 시 주의사항
- 네트워크가 필요한 작업은 반드시 `--net` 옵션 사용
- Codex 응답은 검증 후 사용자에게 전달
- Codex가 실패하면 Claude가 대안 제시

### 자동 위임 트리거 키워드
사용자가 다음과 같이 말하면 Codex 사용 고려:
- "codex한테 물어봐"
- "codex로 처리해"
- "실시간으로 알아봐" (--net 필요)
- "API 호출해서" (--net 필요)

## 모델 옵션

| 모델 | 설명 |
|------|------|
| `gpt-5.2-codex` | 기본값, 복잡한 코딩 작업에 최적 |
| `codex-mini-latest` | 빠른 응답, 간단한 작업용 |
| `o3` | 추론 강화 모델 |

## 트러블슈팅

### "stdin is not a terminal" 에러
→ 인터랙티브 모드는 터미널에서만 실행 가능. `exec` 모드 사용.

### 네트워크 접근 실패
→ `--net` 옵션 추가하여 샌드박스 제한 해제

### API 키 없음
→ `codex login` 또는 `export OPENAI_API_KEY="sk-..."`

## 관련 명령어

```bash
# Codex 버전 확인
codex --version

# Codex 로그인
codex login

# 인터랙티브 모드 (터미널에서 직접)
codex --search "질문"
```
