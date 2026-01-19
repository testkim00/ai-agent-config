# WERPBiz 데이터베이스 스키마

ERP 시스템 데이터베이스입니다.

## 테이블 접두어 규칙

| 접두어 | 의미 | 설명 |
|--------|------|------|
| hri | 인사정보 | 정규직 인사 관련 |
| hrd | 우리관리 도급 인사정보 | 우리관리 도급직원 인사 관련 |
| org | 조직/부서 | 부서, 조직 관련 |
| smb | 사업장 | 사업장 정보 관련 |
| snc | SNC 도급 | SNC 도급 관련 |
| com | 공통 | 공통코드 등 |

---

## 테이블 목록

### 인사 관련 (hri)

| 테이블명 | 자연어 표현 | 설명 |
|----------|------------|------|
| hriMaster | 인사정보 마스터, 인사마스터, 직원정보, 사원정보 | 정규직 직원 기본 정보 |
| hriLaborContract | 근로계약, 근로계약정보 | 근로계약 정보 |

### 우리관리 도급 인사 관련 (hrd)

| 테이블명 | 자연어 표현 | 설명 |
|----------|------------|------|
| hrdEmpMaster | 우리관리 도급직원마스터, 우리관리 도급인사마스터, 도급직원, 도급직원마스터 | 우리관리 도급 직원 기본 정보 |
| hrdEmpHis | 우리관리 도급직원이력, 우리관리 도급인사이력, 도급직원이력 | 우리관리 도급 직원 히스토리 |

### 조직/부서 관련 (org)

| 테이블명 | 자연어 표현 | 설명 |
|----------|------------|------|
| orgDeptMaster | 부서마스터, 부서정보, 소속본부 | 부서/본부 정보 |

### 사업장 관련 (smb)

| 테이블명 | 자연어 표현 | 설명 |
|----------|------------|------|
| smbSiteMaster | 사업장마스터, 사업장정보 | 사업장 기본 정보 |

### SNC 도급 관련 (snc)

| 테이블명 | 자연어 표현 | 설명 |
|----------|------------|------|
| sncEmpMaster | SNC직원마스터, SNC인사마스터 | SNC 직원 기본 정보 |
| sncEmpHis | SNC직원이력, SNC인사이력 | SNC 직원 히스토리 |
| sncSiteContractMaster | SNC사업장계약, SNC계약정보 | SNC 사업장 계약 정보 |

### 공통 (com)

| 테이블명 | 자연어 표현 | 설명 |
|----------|------------|------|
| comCodeMaster | 공통코드, 코드마스터 | 공통 코드 정보 |

### 시스템 (sys)

| 테이블명 | 자연어 표현 | 설명 |
|----------|------------|------|
| sysUserMaster | 사용자마스터, 시스템사용자, 로그인계정 | 시스템 사용자 계정 정보 |

---

## 테이블 상세

### hriMaster (인사정보 마스터)

정규직 직원의 기본 인사 정보를 담고 있는 마스터 테이블입니다.

#### 주요 컬럼

| 컬럼명 | 타입 | 자연어 표현 | 설명 |
|--------|------|------------|------|
| emp_id | int | 사번, 직원번호 | 직원 고유 ID |
| emp_name | nvarchar | 이름, 직원명, 성명 | 직원 이름 |
| emp_name_eng | nvarchar | 영문이름 | 영문 이름 |
| social_num | varchar | 주민번호 | 주민등록번호 |
| birthday | varchar | 생년월일, 생일 | 생년월일 |
| gender | varchar | 성별 | 성별 (M/F) |
| first_enter_date | varchar | 최초입사일, 입사일 | 최초 입사 일자 |
| retire_date | varchar | 퇴사일, 퇴직일 | 퇴직 일자 |
| emp_type | varchar | 직원유형, 고용형태 | 정규직/계약직 등 |
| emp_status | varchar | 재직상태, 상태 | WORK(재직), RETI(퇴직) |
| dept_id | int | 부서ID, 부서번호 | 소속 부서 ID |
| site_id | int | 사업장ID | 사업장 ID |
| duty_code | varchar | 직책코드, 직책 | 직책 코드 |
| position_code | varchar | 직급코드, 직급 | 직급 코드 |
| mobile_no | varchar | 휴대폰, 핸드폰, 연락처 | 휴대폰 번호 |
| email | varchar | 이메일 | 이메일 주소 |

#### 자주 사용하는 조건

| 자연어 표현 | SQL 조건 |
|------------|----------|
| 재직중인, 현재 직원 | `emp_status = 'WORK'` |
| 퇴직한, 퇴사한 | `emp_status = 'RETI'` |

---

### orgDeptMaster (부서 마스터)

부서/본부 조직 정보 테이블입니다.

#### 주요 컬럼

| 컬럼명 | 타입 | 자연어 표현 | 설명 |
|--------|------|------------|------|
| dept_id | int | 부서ID, 부서번호 | 부서 고유 ID |
| dept_name | nvarchar | 부서명, 부서이름 | 부서 이름 |
| dept_abbreviation | nvarchar | 부서약칭 | 부서 약칭 |
| parent_dept | int | 상위부서, 소속본부 | 상위 부서 ID |
| dept_category | varchar | 부서구분 | FAMILY, BIZ, SECT 등 |
| leader_emp | int | 부서장, 팀장 | 부서장 사번 |
| sales_dept_yn | varchar | 영업부서여부 | Y/N |
| snc_dept_yn | varchar | SNC부서여부 | Y/N |
| use_yn | varchar | 사용여부 | Y/N |

---

### smbSiteMaster (사업장 마스터)

사업장 기본 정보 테이블입니다.

#### 주요 컬럼

| 컬럼명 | 타입 | 자연어 표현 | 설명 |
|--------|------|------------|------|
| site_id | int | 사업장ID | 사업장 고유 ID |
| site_name | nvarchar | 사업장명, 현장명 | 사업장 이름 |
| address | nvarchar | 주소 | 사업장 주소 |
| phone_no | varchar | 전화번호 | 사업장 전화번호 |
| dept_id | int | 소속부서 | 담당 부서 ID |
| head_emp_id | int | 관리소장, 현장소장 | 관리소장 사번 |
| mng_status | varchar | 관리상태 | MANAGE(관리중) 등 |
| household_cnt | int | 세대수 | 세대 수 |
| contract_start_date | varchar | 계약시작일 | 계약 시작일 |
| contract_end_date | varchar | 계약종료일 | 계약 종료일 |
| building_use_type | varchar | 건물용도 | A(아파트) 등 |

---

### comCodeMaster (공통코드 마스터)

시스템 공통 코드 테이블입니다.

#### 주요 컬럼

| 컬럼명 | 타입 | 자연어 표현 | 설명 |
|--------|------|------------|------|
| group_code | varchar | 그룹코드 | 코드 그룹 |
| sub_code | varchar | 서브코드 | 세부 코드 |
| code_name | nvarchar | 코드명, 코드이름 | 코드 이름 |
| use_yn | varchar | 사용여부 | Y/N |

---

### hriLaborContract (근로계약 정보)

직원 근로계약 정보 테이블입니다.

#### 주요 컬럼

| 컬럼명 | 타입 | 자연어 표현 | 설명 |
|--------|------|------------|------|
| emp_id | int | 사번 | 직원 사번 |
| contract_seq | int | 계약순번 | 계약 순번 |
| dept_id | int | 부서ID | 소속 부서 |
| site_id | int | 사업장ID | 근무 사업장 |
| labor_contract_type | varchar | 계약유형 | D(도급), W(직영) 등 |
| contract_date | varchar | 계약일 | 계약 일자 |
| contract_start_date | varchar | 계약시작일 | 계약 시작일 |
| contract_end_date | varchar | 계약종료일 | 계약 종료일 |
| monthly_base_pay_amt | numeric | 기본급 | 월 기본급 |
| monthly_total_pay_amt | numeric | 총급여, 월급 | 월 총 급여 |

---

### hrdEmpMaster / hrdEmpHis (우리관리 도급 직원 마스터/이력)

우리관리 도급 직원 정보 테이블입니다. (hrdEmpMaster와 hrdEmpHis 구조 동일)

#### 주요 컬럼

| 컬럼명 | 타입 | 자연어 표현 | 설명 |
|--------|------|------------|------|
| emp_id | int | 사번 | 직원 사번 |
| site_id | varchar | 사업장ID | 근무 사업장 |
| dept_id | varchar | 부서ID | 소속 부서 |
| job_code | varchar | 직무코드 | 직무 코드 |
| duty_code | varchar | 직책코드 | 직책 코드 |
| enter_date | varchar | 입사일 | 입사 일자 |
| retire_date | varchar | 퇴사일 | 퇴사 일자 |
| emp_status | varchar | 재직상태 | WORK/RETI |
| account | nvarchar | 계좌번호 | 급여 계좌 |

---

### sncEmpMaster (SNC 직원 마스터)

SNC 도급 직원 정보 테이블입니다.

#### 주요 컬럼

| 컬럼명 | 타입 | 자연어 표현 | 설명 |
|--------|------|------------|------|
| emp_id | varchar | 사번 | 직원 사번 |
| emp_name | nvarchar | 이름, 직원명 | 직원 이름 |
| site_id | varchar | 사업장ID | 근무 사업장 |
| emp_status | varchar | 재직상태 | WORK/RETI |
| job_code | varchar | 직무코드 | 직무 코드 |
| duty_code | varchar | 직책코드 | 직책 코드 |
| enter_date | varchar | 입사일 | 입사 일자 |
| retire_date | varchar | 퇴사일 | 퇴사 일자 |
| social_num | varchar | 주민번호 | 주민등록번호 |
| phone_no | varchar | 연락처 | 휴대폰 번호 |

---

### sncEmpHis (SNC 직원 이력)

SNC 직원 근무 이력 테이블입니다.

#### 주요 컬럼

| 컬럼명 | 타입 | 자연어 표현 | 설명 |
|--------|------|------------|------|
| emp_id | varchar | 사번 | 직원 사번 |
| seq | int | 순번 | 이력 순번 |
| site_id | varchar | 사업장ID | 근무 사업장 |
| enter_date | varchar | 입사일 | 입사 일자 |
| retire_date | varchar | 퇴사일 | 퇴사 일자 |
| contract_start_date | varchar | 계약시작일 | 계약 시작일 |
| contract_end_date | varchar | 계약종료일 | 계약 종료일 |
| monthly_salary | decimal | 월급여 | 월 급여 |

---

### sncSiteContractMaster (SNC 사업장 계약)

SNC 사업장 계약 정보 테이블입니다.

#### 주요 컬럼

| 컬럼명 | 타입 | 자연어 표현 | 설명 |
|--------|------|------------|------|
| HCODE | varchar | H코드 | 사업장 코드 |
| site_name | nvarchar | 사업장명 | 사업장 이름 |
| contract_type | varchar | 계약유형 | 계약 유형 |
| p_cnt | int | 인원수 | 배치 인원 |
| sales | decimal | 매출 | 매출액 |
| contract_start_date | varchar | 계약시작일 | 계약 시작일 |
| contract_end_date | varchar | 계약종료일 | 계약 종료일 |
| dept_id | varchar | 부서ID | 담당 부서 |
| mng_status | varchar | 관리상태 | 관리 상태 |

---

### sysUserMaster (사용자 마스터)

시스템 로그인 계정 정보 테이블입니다. ERP/그룹웨어 등 시스템 접속용 계정을 관리합니다.

#### 주요 컬럼

| 컬럼명 | 타입 | 자연어 표현 | 설명 |
|--------|------|------------|------|
| user_id | varchar | 사용자ID, 로그인ID | 시스템 로그인 ID (두레이 등 외부 연동용) |
| user_no | varchar | 사용자번호 | 사용자 번호 |
| user_name | nvarchar | 사용자명 | 사용자 이름 |
| emp_id | int | 사번 | 연결된 직원 사번 (hriMaster와 조인 키) |
| user_category | varchar | 사용자구분 | SITEUSER(현장), HQUSER(본사) 등 |
| apply_start_date | varchar | 적용시작일 | 계정 적용 시작일 |
| apply_end_date | varchar | 적용종료일 | 계정 적용 종료일 |
| erp_user_yn | varchar | ERP사용여부 | Y/N |
| gw_user_yn | varchar | GW사용여부 | Y/N |

---

## 자주 사용하는 조인 패턴

### 본사직원 조회 (hriMaster 기준)

본사 재직 직원의 상세 정보를 조회할 때 사용하는 조인 패턴입니다.

```sql
SELECT
    h.emp_id AS 사번,
    h.emp_name AS 이름,
    s.user_id AS 사용자ID,      -- 두레이 등 외부 연동용
    d.dept_name AS 부서,
    pos.code_name AS 직급,
    duty.code_name AS 직책
FROM hriMaster h
LEFT JOIN sysUserMaster s ON h.emp_id = s.emp_id           -- 사용자 계정 정보
LEFT JOIN orgDeptMaster d ON h.dept_id = d.dept_id         -- 부서 정보
LEFT JOIN comCodeMaster pos ON h.position_code = pos.sub_code
    AND pos.group_code = 'HRI008'                          -- 직급 코드
LEFT JOIN comCodeMaster duty ON h.duty_code = duty.sub_code
    AND duty.group_code = 'HRI007'                         -- 직책 코드
WHERE h.emp_status = 'WORK'                                -- 재직자
  AND h.work_place_type = 'HQ'                             -- 본사 근무
ORDER BY d.dept_name, h.emp_name
```

#### 공통코드 참조

| group_code | 설명 | 예시 |
|------------|------|------|
| HRI007 | 직책 | 팀장, 팀원, 본부장, 사원 등 |
| HRI008 | 직급 | 사원, 대리, 과장, 매니저, 책임 매니저 등 |

#### 조건 설명

| 컬럼 | 값 | 설명 |
|------|-----|------|
| work_place_type | 'HQ' | 본사 근무자 |
| work_place_type | 'SITE' | 현장 근무자 |
| emp_status | 'WORK' | 재직중 |
| emp_status | 'RETI' | 퇴직 |

---

## 참고사항

- MSSQL 2014이므로 `LIMIT` 대신 `TOP` 사용
- 날짜 컬럼은 대부분 varchar 타입 (YYYYMMDD 형식)
- 한글 데이터는 nvarchar 타입
- emp_status 값: WORK(재직), RETI(퇴직), POOL(대기) 등
