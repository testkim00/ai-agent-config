---
name: migration
description: Analyze legacy WOORI/WERPBiz WinForms modules for migration into WooriErpClient (Vue 3) and WooriErp (.NET) using source code, stored procedures, tables, and live DB metadata. Use when the task is written like `/migration` or `/migration <folder-name>`, or when the user wants implementation-ready migration documents, menu/screen inventory, popup flow analysis, DB procedure/table verification, or target-project-fit analysis for a legacy module.
---

# Migration

## Goal

Produce implementation-ready migration documentation for a legacy `WOORI/WERPBiz` module so another agent can build the target feature in `WooriErpClient` and `WooriErp` without reverse-engineering the legacy project again.

## Invocation

- Interpret `/migration <folder-name>` as: analyze everything recursively under that folder from the current workspace.
- Interpret `/migration` with no folder argument as: analyze everything under the current working directory.
- When the folder name is not an exact path, resolve it against the current workspace before continuing.
- Treat the resolved target folder as the scope boundary unless the user explicitly expands it.

## Workflow

### 1. Fix the migration boundary first

- Identify the exact legacy module root, solution, and project under `WOORI/...`.
- Inventory all forms, popups, helper classes, shared utilities, and designer files.
- Separate visible user screens from hidden admin tools, batch screens, incomplete features, and shared selectors.
- Treat “all functional coverage” as the scope, not just the main form.

### 2. Read the target projects before drafting web design

- Inspect `WooriErpClient` routing, menu loading, popup hosting, and HTTP service usage.
- Inspect `WooriErp` controller, service, DTO, EF Core, and write-envelope patterns.
- Prefer the actual target-project conventions over generic SPA/REST assumptions.
- Record project-specific constraints early because they change route naming, file placement, DTO shape, and save flow.

For this environment, always verify at least these areas:

- Client: router, dynamic view resolution, popup host, shared API service
- Server: representative controller/service pair, `WriteRequestEnvelope<T>`, `DbContext`, existing `WERPBiz` models

### 3. Build the screen and flow inventory

- Derive the current menu tree, entry points, main forms, popup relationships, and cross-screen callbacks.
- For each screen, document purpose, filters, fields, buttons, grid actions, save behavior, and child popups.
- Distinguish “read-only inquiry”, “editable management”, “report/batch”, and “lookup popup” because the web UI should split them.
- Do not mirror WinForms tabs or modal nesting blindly if the web target should separate them into routes or pages.

If producing a full document set, read `references/document-set.md`.

### 4. Verify DB behavior whenever procedures or tables matter

- Use the `db-query` skill when procedure SQL, schema metadata, PKs, row counts, or table dependencies affect the migration.
- Export raw artifacts under the module’s migration doc folder, typically `docs/<module>-migration/db/`.
- Capture procedure list, parameters, dependencies, table columns, and table row counts before summarizing.
- Read raw SQL for the procedures with the highest business impact instead of trusting only metadata.

If DB-backed analysis is needed, read `references/db-verification.md`.

### 5. Treat live DB as the source of truth

- Prefer `live DB export > raw SQL > WinForms call flow > current EF models`.
- Flag any mismatch between live DB types/keys and current `WooriErp` EF models.
- Pay special attention to mixed key types, multi-table side effects, status transitions, backup/delete flows, file metadata coupling, encryption, and external API usage.
- Call out hidden or unresolved objects separately instead of silently omitting them.

### 6. Convert legacy behavior into target-ready design

- Replace `@p_work_type` multiplexed procedures with feature-oriented API candidates.
- Split UI by task: inquiry, management, report, batch, and lookup.
- Keep business semantics and validation rules, but do not preserve legacy internal structure if it conflicts with Vue/.NET implementation quality.
- Recommend transaction boundaries and aggregate ownership where stored procedures currently update multiple tables.

### 7. Write for the next implementer

- Assume the next reader has the source tree but not your current memory.
- State what is confirmed, what is inferred, and what remains unresolved.
- Link raw DB exports and highlight the exact documents the implementer must read first.
- Surface the highest-risk migration points near the top instead of burying them in appendices.

## Non-negotiables

- Cover all legacy functionality under the requested module, including hidden or low-usage screens.
- Separate current UI structure from target web IA; do not force a one-to-one WinForms clone.
- Document popup and child-grid behavior explicitly because that is where most save side effects hide.
- When DB access is available, do not stop at source-code assumptions if stored procedures drive behavior.
- When DB access is unavailable, say so explicitly and list what could not be verified.

## Deliverables

- A migration README that explains scope, source-of-truth order, and reading order
- Menu/screen/popup/flow documents
- Procedure and data-contract documents
- Target-project-fit and implementation-blueprint documents
- DB-backed procedure/table notes when live schema inspection is possible

## References

- `references/document-set.md`: Required migration document set and content checklist
- `references/db-verification.md`: DB extraction checklist and what to record from `WERPBiz`
