#!/usr/bin/env python3
"""
DB Query Script - 여러 DB 타입을 지원하는 범용 쿼리 실행 스크립트
사용법: python3 query.py {DB_PREFIX} "{SQL_QUERY}"
        python3 query.py --list  # 등록된 DB 목록 확인
"""

import sys
import os
from pathlib import Path


def load_env():
    """~/.claude/.env 파일에서 환경변수 로드"""
    env_path = Path.home() / ".claude" / ".env"
    env_vars = {}

    if not env_path.exists():
        print(f"Error: {env_path} 파일이 없습니다.", file=sys.stderr)
        sys.exit(1)

    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip()

    return env_vars


def get_db_config(env_vars, prefix):
    """특정 접두어의 DB 설정 가져오기"""
    config = {}
    keys = ["TYPE", "HOST", "PORT", "NAME", "USER", "PASSWORD", "OPTIONS"]

    for key in keys:
        env_key = f"{prefix}_DB_{key}"
        if env_key in env_vars:
            config[key.lower()] = env_vars[env_key]

    if "type" not in config:
        print(f"Error: {prefix}_DB_TYPE이 설정되지 않았습니다.", file=sys.stderr)
        sys.exit(1)

    return config


def list_databases(env_vars):
    """등록된 DB 목록 출력"""
    prefixes = set()
    for key in env_vars:
        if key.endswith("_DB_TYPE"):
            prefix = key.replace("_DB_TYPE", "")
            prefixes.add(prefix)

    if not prefixes:
        print("등록된 DB가 없습니다.")
        return

    print("등록된 DB 목록:")
    print("-" * 50)
    for prefix in sorted(prefixes):
        db_type = env_vars.get(f"{prefix}_DB_TYPE", "unknown")
        db_host = env_vars.get(f"{prefix}_DB_HOST", "unknown")
        db_name = env_vars.get(f"{prefix}_DB_NAME", "unknown")
        print(f"  {prefix}: {db_type} @ {db_host} / {db_name}")


def connect_mssql(config):
    """MSSQL 연결"""
    try:
        import pymssql
    except ImportError:
        print("Error: pymssql이 설치되지 않았습니다. pip install pymssql", file=sys.stderr)
        sys.exit(1)

    options = {}
    if "options" in config:
        for opt in config["options"].split(","):
            if "=" in opt:
                k, v = opt.split("=", 1)
                options[k.strip()] = v.strip()

    return pymssql.connect(
        server=config["host"],
        port=int(config.get("port", 1433)),
        user=config["user"],
        password=config["password"],
        database=config["name"],
        tds_version=options.get("tds_version", "7.3"),
        charset="UTF-8"
    )


def connect_mysql(config):
    """MySQL 연결"""
    try:
        import pymysql
    except ImportError:
        print("Error: pymysql이 설치되지 않았습니다. pip install pymysql", file=sys.stderr)
        sys.exit(1)

    return pymysql.connect(
        host=config["host"],
        port=int(config.get("port", 3306)),
        user=config["user"],
        password=config["password"],
        database=config["name"],
        charset="utf8mb4"
    )


def connect_postgres(config):
    """PostgreSQL 연결"""
    try:
        import psycopg2
    except ImportError:
        print("Error: psycopg2가 설치되지 않았습니다. pip install psycopg2-binary", file=sys.stderr)
        sys.exit(1)

    return psycopg2.connect(
        host=config["host"],
        port=int(config.get("port", 5432)),
        user=config["user"],
        password=config["password"],
        dbname=config["name"]
    )


def execute_query(conn, query, db_type):
    """쿼리 실행 및 결과 출력"""
    cursor = conn.cursor()
    cursor.execute(query)

    # SELECT 쿼리인지 확인
    if cursor.description:
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        if not rows:
            print("결과가 없습니다.")
            return

        # 컬럼 너비 계산
        widths = []
        for i, col in enumerate(columns):
            max_width = len(str(col))
            for row in rows:
                val_len = len(str(row[i]) if row[i] is not None else "NULL")
                max_width = max(max_width, val_len)
            widths.append(min(max_width, 50))  # 최대 50자

        # 헤더 출력
        header = " | ".join(str(col).ljust(widths[i])[:widths[i]] for i, col in enumerate(columns))
        print(header)
        print("-" * len(header))

        # 데이터 출력
        for row in rows:
            row_str = " | ".join(
                str(val if val is not None else "NULL").ljust(widths[i])[:widths[i]]
                for i, val in enumerate(row)
            )
            print(row_str)

        print(f"\n총 {len(rows)}개 행")
    else:
        # INSERT/UPDATE/DELETE
        affected = cursor.rowcount
        conn.commit()
        print(f"쿼리 실행 완료. 영향받은 행: {affected}")

    cursor.close()


def main():
    if len(sys.argv) < 2:
        print("사용법: python3 query.py {DB_PREFIX} \"{SQL_QUERY}\"")
        print("        python3 query.py --list")
        sys.exit(1)

    env_vars = load_env()

    # --list 옵션
    if sys.argv[1] == "--list":
        list_databases(env_vars)
        return

    if len(sys.argv) < 3:
        print("Error: SQL 쿼리를 입력하세요.", file=sys.stderr)
        sys.exit(1)

    prefix = sys.argv[1].upper()
    query = sys.argv[2]

    config = get_db_config(env_vars, prefix)
    db_type = config["type"].lower()

    # DB 타입별 연결
    connectors = {
        "mssql": connect_mssql,
        "mysql": connect_mysql,
        "postgres": connect_postgres,
    }

    if db_type not in connectors:
        print(f"Error: 지원하지 않는 DB 타입입니다: {db_type}", file=sys.stderr)
        print(f"지원 타입: {', '.join(connectors.keys())}")
        sys.exit(1)

    try:
        conn = connectors[db_type](config)
        execute_query(conn, query, db_type)
        conn.close()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
