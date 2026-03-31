---
name: az-app
description: Azure App Service Web App 인벤토리 조회와 운영 배포를 수행할 때 사용한다. Claude의 `/az:app` 명령을 Codex에서 같은 의도로 수행해야 할 때 사용한다. `az-app deploy` 요청이면 현재 레포명을 기준으로 매핑표에서 대상 웹앱을 찾고, 애플리케이션을 publish한 뒤 production 슬롯에 배포한다.
---

# Azure App Service

## 언제 사용하나

- Azure App Service Web App 존재 여부, 상태, 설정을 조회할 때
- 현재 레포를 Azure Web App production에 배포할 때
- 레포와 Azure Web App 간 매핑을 기준으로 배포 대상을 자동 선택해야 할 때
- Static Web Apps가 아니라 App Service 자체를 다뤄야 할 때

## source mapping

- Claude command: `/az:app`

## 프로젝트 매핑

- 레포명과 웹앱 매핑은 [references/project-map.md](references/project-map.md)에서 찾는다.
- `az-app deploy`처럼 대상 앱을 생략한 요청은 현재 작업 디렉터리명을 기준으로 위 매핑표를 먼저 적용한다.
- 현재 프로젝트가 매핑표에 없으면 임의 추정하지 말고 대상 Web App 이름을 짧게 확인한다.

## 기본 규칙

- App Service 배포는 `az webapp deploy`를 사용한다.
- 운영 반영이 목적이면 기본은 production 슬롯이다. 사용자가 명시하지 않는 한 slot 배포로 바꾸지 않는다.
- 먼저 publish artifact를 만든 뒤 배포한다. .NET 프로젝트는 기본적으로 `dotnet publish -c Release -o <publish-dir>`를 사용한다.
- 배포 아티팩트는 publish 디렉터리를 zip으로 묶어서 `az webapp deploy --type zip`으로 올린다.
- 배포 전에 `az webapp show`로 대상 웹앱과 리소스 그룹이 맞는지 확인한다.
- 배포 뒤에는 기본 호스트에 `curl -sI https://<defaultHostName>`로 응답 상태를 확인한다.
- 현재 프로젝트에 `.csproj`가 여러 개면 어떤 프로젝트를 publish할지 짧게 확인한다.

## 실행 절차

1. 사용자의 요청을 `inventory`, `deploy`, `config`, `slot` 중 하나로 분류한다.
2. 배포 요청이면 현재 작업 디렉터리명으로 매핑표를 조회해 Web App 이름, 리소스 그룹, 구독, 빌드 방식을 결정한다.
3. Azure CLI 로그인 상태와 현재 구독 접근 여부를 확인한다.
4. `az webapp show -g <rg> -n <app>`로 대상 앱이 실제 존재하는지 검증한다.
5. .NET 앱이면 프로젝트 루트의 `.csproj`를 찾고 `dotnet publish -c Release -o <tmp-publish-dir>`를 실행한다.
6. publish 결과를 zip으로 묶는다.
7. `az webapp deploy -g <rg> -n <app> --src-path <zip> --type zip --restart true`로 production 슬롯에 배포한다.
8. 필요하면 `az webapp restart -g <rg> -n <app>`를 추가로 수행한다.
9. `az webapp show --query defaultHostName -o tsv`와 `curl -sI`로 배포 후 응답을 확인한다.
10. 성공 시 배포 대상, 호스트명, 검증 결과를 요약한다.

## 사용자에게 물어봐야 하는 경우

- 현재 프로젝트 디렉터리명이 매핑표에 없어서 대상 Web App을 자동 결정할 수 없을 때
- `.csproj`가 여러 개라 어떤 프로젝트를 publish해야 하는지 애매할 때
- 사용자가 production이 아닌 slot 배포를 원할 가능성이 있을 때
- 대상 구독이나 리소스 그룹이 매핑표와 실제 Azure 상태에서 어긋날 때

## 하지 말아야 할 것

- 현재 프로젝트 매핑이 있는데도 임의의 다른 Web App에 배포하지 않는다.
- publish 없이 소스 디렉터리를 그대로 배포했다고 가정하지 않는다.
- production 반영 요청인데 slot에 올리고 끝내지 않는다.
- Azure 리소스 존재 확인 없이 배포를 강행하지 않는다.
