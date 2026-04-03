---
name: az-swa
description: Azure Static Web Apps 리소스 조회, 배포, 커스텀 도메인/SSL, RBAC 작업을 수행할 때 사용한다. Claude의 `/az:swa` 명령을 Codex에서 같은 의도로 수행해야 할 때 사용한다.
---

# Azure SWA

## 언제 사용하나

- Azure Static Web Apps 인벤토리, 상태, 환경 정보를 조회하거나 동기화할 때
- SWA CLI로 Static Web Apps에 배포할 때
- 커스텀 도메인, SSL 상태, RBAC 권한을 점검하거나 변경할 때
- App Service나 APIM이 아니라 Static Web Apps 자체를 다뤄야 할 때

## source mapping

- Claude command: `/az:swa`
- Source file: `claude/commands/az/swa.md`

## 프로젝트 매핑

- 현재 작업 디렉터리명이 `WooriErpClient`면 SWA 리소스는 `swa-werp-client`, 토큰 키는 `SWA_WERP_CLIENT_API_TOKEN`으로 본다.
- 현재 작업 디렉터리명이 `WooriDataPlatformClient`면 SWA 리소스는 `swa-dataplatform-client`, 토큰 키는 `SWA_DATAPLATFORM_CLIENT_API_TOKEN`으로 본다.
- `az-swa deploy`처럼 대상 앱을 생략한 요청은 현재 작업 디렉터리명을 기준으로 위 매핑을 먼저 적용한다.
- 현재 프로젝트가 매핑표에 없으면 임의 추정하지 말고 대상 SWA 이름 또는 토큰 키를 짧게 확인한다.

## 기본 규칙

- Azure Static Web Apps 작업은 `az staticwebapp`와 `swa` CLI를 구분해서 사용한다.
- 배포는 `swa deploy`를 사용하고, 운영 반영이 목적이면 항상 `--env production`을 명시한다.
- 배포 요청에서는 현재 프로젝트에 매핑된 `.env` 토큰 키를 먼저 찾고, 토큰이 있으면 `--deployment-token`을 우선 사용한다.
- `swa login` 또는 `swa deploy`가 프로젝트 `.env`를 덮어쓸 수 있으므로, 추적 파일이면 작업 후 원복 여부를 확인한다.
- `staticwebapp.config.json`은 앱 루트 기준으로 자동 포함된다고 가정하고, GitHub Actions 예외만 따로 판단한다.
- RBAC 범위는 `Microsoft.Web/staticSites` 기준으로 잡고, App Service 범위와 혼동하지 않는다.

## 실행 절차

1. 사용자의 요청을 `inventory`, `deploy`, `domain`, `rbac` 중 하나로 분류한다.
2. 인벤토리가 필요하면 캐시 파일과 마지막 동기화 시점을 먼저 확인한다.
3. 캐시가 오래됐거나 사용자가 동기화를 명시하면 `az staticwebapp list`와 `az staticwebapp hostname list`로 최신 정보를 갱신한다.
4. 배포 요청이면 현재 작업 디렉터리명으로 프로젝트 매핑을 확인하고, 대응되는 SWA 리소스명과 `.env` 토큰 키를 먼저 결정한다.
5. 프로젝트 루트의 `swa-cli.config.json`이 있으면 config 이름과 `appName`, `resourceGroup`, `outputLocation`을 읽고, 없으면 출력 디렉터리만 별도로 판단한다.
6. config가 여러 개면 대상 config를 짧게 확인한 뒤, `build`, `build:pwa`, `skip` 중 빌드 방식을 정해서 배포한다.
7. 매핑된 `.env` 토큰 키에서 deployment token을 읽을 수 있으면 `swa deploy --config-name <name> --deployment-token "$TOKEN" --env production` 형식을 우선 사용한다.
8. `swa-cli.config.json`이 없으면 `swa deploy <output-dir> --deployment-token "$TOKEN" --env production` 형식으로 배포한다.
9. 토큰 키가 없거나 현재 프로젝트가 매핑표에 없을 때만 대상 SWA 이름 또는 사용할 토큰 키를 짧게 확인한다.
10. 배포 뒤에는 기본 호스트에 `curl -sI`로 응답 상태를 확인하고, `.env`가 오염됐으면 원복한다.
11. 도메인 작업이면 먼저 `az staticwebapp hostname list`로 현재 상태를 보고, 신규 등록 전에는 `dig +short <hostname> CNAME`으로 DNS를 검증한다.
12. SSL 상태 점검은 hostname 상태 조회 또는 `curl -v https://<hostname>` 결과로 확인한다.
13. RBAC 작업이면 SWA scope를 구성하고, 필요 시 사용자 principal ID를 조회한 뒤 role assignment를 생성하거나 조회한다.

## 사용자에게 물어봐야 하는 경우

- 현재 프로젝트 디렉터리명이 매핑표에 없어서 SWA 리소스나 토큰 키를 자동 결정할 수 없을 때
- 매핑된 토큰 키가 `.env`에 없을 때
- `swa-cli.config.json`에 config가 둘 이상이라 자동 선택이 애매할 때
- `build`, `build:pwa`, `skip` 중 어떤 배포 흐름을 써야 하는지 불분명할 때
- 사용자가 운영 또는 production 배포를 명시했고, 즉시 반영 여부를 재확인해야 할 때
- 대상 SWA 이름, 구독, 리소스 그룹, 도메인이 불명확할 때

## 하지 말아야 할 것

- 현재 프로젝트 매핑이 있는데도 임의의 다른 SWA 토큰을 사용하지 않는다.
- `az staticwebapp deploy`가 있다고 가정하지 않는다.
- `--env production` 없이 운영 반영을 기대하지 않는다.
- DNS 검증 없이 커스텀 도메인 등록을 강행하지 않는다.
- App Service용 RBAC 범위를 SWA 리소스에 그대로 적용하지 않는다.
- `.env` 변경 가능성을 무시한 채 배포를 끝내지 않는다.
