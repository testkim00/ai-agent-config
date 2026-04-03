# Orientation Template

Use this template for either:

- a short in-chat orientation
- a persistent `PROJECT_STRUCTURE.md`

Keep it compact. Drop sections that are not relevant. Do not pad the output with exhaustive trees or low-signal file lists.

## Quick Briefing Template

- Project: one-sentence summary of what the repository does
- Repo shape: single app, client/server split, monorepo, multi-service, library, or mixed
- Primary stack: languages, frameworks, package managers, and notable infrastructure
- Runbook: install, dev, build, test, and migration commands that are actually supported by repo files
- Start here: 3-5 files a fresh session should read first
- Main modules: top-level areas and what each one owns
- Boot flow: entry point to routing or request handling to business logic to persistence
- Editing cautions: shared modules, generated code, migrations, auth, deployment-sensitive code, or config traps
- Unknowns: gaps that the current repository files did not fully answer

## Persistent Note Template

```md
# Project Structure

## Summary
- Purpose:
- Repo shape:
- Primary stack:

## Runbook
- Install:
- Dev:
- Build:
- Test:
- Lint:
- Migrations or codegen:

## Start Here
- `path/to/file`: why this file matters
- `path/to/file`: why this file matters
- `path/to/file`: why this file matters

## Directory Map
| Path | Responsibility | Representative files |
| --- | --- | --- |
| `src/...` | ... | `...`, `...` |

## Boot And Request Flow
1. Entry point:
2. Startup and registration:
3. Routing or command dispatch:
4. Business logic:
5. Data access or external integration:

## Major Domains
| Domain | Responsibility | Key files |
| --- | --- | --- |
| ... | ... | `...` |

## Editing Cautions
- ...
- ...

## Open Questions
- ...
```

## Quality Bar

- Prefer evidence from files over inference.
- Prefer representative files over long directory dumps.
- Prefer module responsibilities over filename repetition.
- Prefer concrete cautions over generic statements.
