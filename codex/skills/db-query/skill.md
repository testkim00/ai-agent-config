---
name: db-query
description: Query configured databases using connection info from `~/.codex/.env`. Use when the user asks to inspect schema, run SQL, or verify data in DBs such as `ERP`.
---

# DB Query

Use this skill when the user asks to inspect a database, verify table data, or run SQL against a configured DB.

## Setup

- Read `~/.codex/.env` and resolve the DB prefix from the request.
- Supported connection keys:
  - `{PREFIX}_DB_TYPE`
  - `{PREFIX}_DB_HOST`
  - `{PREFIX}_DB_PORT`
  - `{PREFIX}_DB_NAME`
  - `{PREFIX}_DB_USER`
  - `{PREFIX}_DB_PASSWORD`

## Workflow

1. Identify the target DB prefix.
   - Example: `ERP`
2. If the request is ambiguous, check [databases.md](databases.md).
3. If schema context is needed, open the matching file under `schema/`.
4. Translate the user request into SQL.
5. Execute the query with the bundled [query.py](query.py) script.
6. Summarize the result clearly and avoid exposing credentials.

## Execution Rule

Use the bundled script instead of opening DB connections directly when possible.

```bash
python3 query.py "{PREFIX}" "{SQL}"
```

## References

- [databases.md](databases.md): DB name to prefix mapping
- [templates.md](templates.md): template and output guidance
- [query.py](query.py): query execution script

## Notes

- This skill supports both direct query output and template-based export flows.
- If DB access is blocked by the environment, state that clearly and do not pretend the query ran.
- Risky SQL writes are hook-gated. If the query contains `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `TRUNCATE`, DDL, `EXEC`, `CALL`, or runs a `.sql` script, the user must explicitly approve it in the prompt with `SQL_WRITE_OK: <db/reason>` before execution.
