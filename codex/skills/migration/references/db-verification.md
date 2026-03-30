# DB Verification Checklist

Use this reference when the legacy module depends on stored procedures or when the target implementation must follow real `WERPBiz` schema behavior.

## 1. Preparation

- Use the `db-query` skill.
- Load DB connection info from `~/.codex/.env`.
- For `WERPBiz`, the usual prefix is `ERP`.
- If the environment requires approval for network or DB access, request it immediately before continuing.

## 2. Minimum raw exports

Export these artifacts under `docs/<module>-migration/db/`:

- `procedure-index.csv`
- `procedure-parameters.csv`
- `procedure-dependencies.csv`
- `table-list.txt`
- `table-columns.csv`
- `table-rowcounts.csv`
- `stats.json`
- `procedures/*.sql`

## 3. Required questions to answer

### Procedure layer

- Which procedures belong to the module?
- Which are query, write, popup, report, or batch procedures?
- Which procedures multiplex multiple features via `@p_work_type`?
- Which output/error parameters are standardized?
- Which procedures call other procedures?

### Table layer

- Which tables are touched by the high-impact procedures?
- What are the row counts of the main tables?
- What are the PKs of the main tables?
- Are `emp_id`, `site_id`, `seq`, `contract_seq`, and `enter_date` types consistent?
- Which tables are current master, history, file metadata, insurance, vacation, appoint, or temp-import tables?

### Risk layer

- Does the current `WooriErp` EF model match the live DB?
- Are there backup tables, delete-history tables, or sync side effects?
- Are there hidden objects such as lookup tables, views, or helper procedures not visible from screen code?

## 4. What to summarize in the DB document

- Procedure inventory by business role
- `@p_work_type` matrix
- Core table map with row counts and key notes
- Major procedure-to-table dependencies
- Important side effects of save/delete/retire/contract/file flows
- Type mismatches between live DB and existing server models
- Implementation guidance for API split and transaction boundaries

## 5. Source-of-truth rule

When results conflict:

1. live DB metadata
2. raw stored procedure SQL
3. WinForms usage pattern
4. existing EF model files

Do not silently trust EF scaffolding if live DB says otherwise.
