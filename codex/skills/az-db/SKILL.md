---
name: az-db
description: Azure SQL Database의 현재 용량, 할당량, 최대 용량, 상태, SKU를 조회할 때 사용한다. `woori-core-db 용량`처럼 DB 이름 기준으로 현재 사용량을 확인해야 하거나, DB 이름만 받고 Azure SQL Server와 Resource Group을 찾아야 할 때 사용한다.
---

# Azure DB

## 언제 사용하나

- Azure SQL Database의 현재 사용량과 최대 용량을 확인할 때
- `database_size`와 `database_allocated_size`를 구분해서 보고해야 할 때
- DB 이름만 알고 있고, 서버와 리소스 그룹은 스킬이 찾아야 할 때
- Azure SQL Database의 SKU, 상태, 서버, 리소스 그룹을 함께 확인할 때

## source mapping

- Claude command: `/az:db`

## DB 매핑

- 알려진 DB 매핑은 [references/db-map.md](references/db-map.md)에서 먼저 찾는다.
- 요청이 `az-db woori-core-db 용량`처럼 DB 이름만 포함하면 매핑표를 우선 사용한다.
- 매핑표에 없으면 `az sql server list` 후 각 서버의 `az sql db list`를 조회해 DB를 탐색한다.
- DB 이름이 둘 이상 발견되면 임의 선택하지 말고 서버와 리소스 그룹을 짧게 확인한다.

## 기본 규칙

- 이 스킬은 Azure SQL Database 전용이다. SQL Managed Instance, PostgreSQL, MySQL은 이 스킬 범위로 가정하지 않는다.
- 현재 시점의 용량 조회는 `az sql db list-usages`를 우선 사용한다.
- DB 상태, SKU, 최대 용량, 서버 정보는 `az sql db show`로 보강한다.
- 바이트 단위 결과는 사람이 읽기 쉬운 GB로 변환해서 보여준다.
- `database_size`는 실제 사용량, `database_allocated_size`는 할당량이므로 같은 값으로 취급하지 않는다.
- 사용률은 `database_size / limit`와 `database_allocated_size / limit` 두 값을 구분해 계산한다.

## 실행 절차

1. 사용자의 요청을 `usage`, `show`, `inventory` 중 하나로 분류한다.
2. 요청에 DB 이름이 있으면 [references/db-map.md](references/db-map.md)에서 서버, 리소스 그룹, 구독을 먼저 찾는다.
3. 매핑이 없으면 아래 순서로 탐색한다.
   - `az sql server list -o table`
   - 각 후보 서버별 `az sql db list -g <rg> -s <server> -o table`
4. 대상 DB가 확인되면 `az sql db show -g <rg> -s <server> -n <db>`로 기본 메타데이터를 확인한다.
5. 용량 요청이면 `az sql db list-usages -g <rg> -s <server> -n <db> -o json`를 실행한다.
6. `database_size`, `database_allocated_size`, `limit`를 추출해 GB와 사용률로 계산한다.
7. 결과는 아래 정보를 포함해 요약한다.
   - DB 이름
   - SQL Server
   - Resource Group
   - Subscription
   - SKU 또는 Service Objective
   - 실제 사용량(`database_size`)
   - 할당량(`database_allocated_size`)
   - 최대 용량(`limit`)
   - 실제 사용률과 할당 사용률

## 응답 형식 가이드

- `woori-core-db`
- Server: `woori-sql-01`
- Resource Group: `rg-woori-infra`
- Current Used: `1.40 GB / 250.00 GB (0.56%)`
- Current Allocated: `2.06 GB / 250.00 GB (0.82%)`
- SKU: `Standard`

## 사용자에게 물어봐야 하는 경우

- DB 이름이 둘 이상 서버에서 발견될 때
- 매핑표에도 없고 탐색 결과에도 없을 때
- 사용자가 “현재 용량”이 아니라 기간별 추이나 경보 임계값을 원할 때
- 대상이 Azure SQL Database가 아니라 Managed Instance/PostgreSQL/MySQL일 가능성이 있을 때

## 하지 말아야 할 것

- `database_allocated_size`를 실제 사용량이라고 보고하지 않는다.
- 서버와 리소스 그룹을 확인하지 않은 채 DB를 추정하지 않는다.
- `az sql db show`만 보고 현재 사용량을 판단하지 않는다.
- 이 스킬에서 SKU 변경, 방화벽 변경, 백업 복원 같은 수정 작업까지 확장하지 않는다.
