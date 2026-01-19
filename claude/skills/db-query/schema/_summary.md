# DB 스키마 요약 (Quick Reference)

> 이 파일을 먼저 읽고, 상세 정보 필요 시 개별 스키마 파일 참조

## WERPBiz (ERP)

| 접두어 | 의미 | 주요 테이블 |
|--------|------|------------|
| hri | 정규직 인사 | hriMaster, hriLaborContract |
| hrd | 우리관리 도급 | hrdEmpMaster, hrdEmpHis |
| snc | SNC 도급 | sncEmpMaster, sncSiteContractMaster |
| smb | 사업장 | smbSiteMaster |
| org | 조직/부서 | orgDeptMaster |
| com | 공통코드 | comCodeMaster |
| sys | 시스템 | sysUserMaster |

### 자주 쓰는 테이블

| 테이블 | 용도 | 주요 컬럼 |
|--------|------|----------|
| hriMaster | 정규직 직원 | emp_id, emp_name, dept_id, emp_status |
| hrdEmpMaster | 우리관리 도급직원 | emp_id, site_id, enter_date, emp_status |
| sncEmpMaster | SNC 직원 | emp_id, emp_name, site_id, emp_status |
| smbSiteMaster | 사업장 | site_id, site_name, address, contract_start_date |
| sncSiteContractMaster | SNC 계약 | HCODE, site_name, contract_start_date, p_cnt |
| orgDeptMaster | 부서 | dept_id, dept_name, parent_dept |

### 공통 조건

| 자연어 | SQL |
|--------|-----|
| 재직중 | `emp_status = 'WORK'` |
| 퇴직 | `emp_status = 'RETI'` |
| 본사 | `work_place_type = 'HQ'` |
| 현장 | `work_place_type = 'SITE'` |

### DB별 문법

| DB | 상위 N개 | 날짜 형식 |
|----|---------|----------|
| MSSQL | `TOP N` | varchar (YYYYMMDD) |
| MySQL | `LIMIT N` | - |

## 스키마 확인 규칙

```sql
-- 컬럼 확인 시 항상 TOP 1 사용
SELECT TOP 1 * FROM 테이블명

-- MySQL의 경우
SELECT * FROM 테이블명 LIMIT 1
```

## 상세 스키마

- WERPBiz: `./WERPBiz.md`
