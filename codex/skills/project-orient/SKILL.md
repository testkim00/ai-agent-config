---
name: project-orient
description: Reconstruct project context quickly in a fresh Codex session by mapping repository structure, stack, entry points, run and test commands, module boundaries, and editing cautions from local files. Use when the user asks to understand a project, orient on a repository, summarize structure, decide where to start reading, create or refresh onboarding notes, or says things like "프로젝트 파악해줘", "구조 브리핑해줘", or "어디부터 읽어야 해?".
---

# Project Orient

## Overview

Use this skill to rebuild enough project context to work safely without rereading the entire repository. Prefer a short, high-signal orientation that explains how the project starts, how it is organized, how to run it, and where changes are risky.

## Operating Principles

- Reconstruct working context, not a full file inventory.
- Prefer existing documentation when it exists, but verify it against current files before trusting it.
- Read the smallest set of files that explains boot flow, code organization, and editing constraints.
- Ignore generated, vendored, build, cache, and dependency directories unless they are part of runtime or build logic.
- State uncertainty explicitly when the repository does not fully answer a question.

## Orientation Workflow

### 1. Detect Repository Shape

- Identify the project root from `.git` and primary manifest files.
- Classify the repository as single app, multi-service, monorepo, client/server split, library, or mixed workspace.
- Detect the primary languages, frameworks, package managers, and deployment surfaces.

### 2. Read High-Signal Files First

Start from the smallest set of files that explains how the repository works:

- `README*`, root manifests, workspace config, solution files, and task runners
- CI, Docker, compose, or deployment config when they define real run paths
- env examples and non-secret config files
- application entry points such as `main.*`, `index.*`, `Program.cs`, `App.vue`, `app.py`, `manage.py`
- routing, dependency injection, boot, plugin, middleware, or startup registration files

### 3. Map Boot and Runtime Flow

- Identify how the app starts and which files control startup order.
- Identify how requests, routes, pages, jobs, or commands reach the main business logic.
- Identify how configuration, auth, HTTP clients, data access, and shared globals are wired.

### 4. Map Code Organization

Summarize only the directories and modules that matter for future edits:

- top-level apps and packages
- shared libraries and common components
- feature or domain modules
- infrastructure layers such as API clients, persistence, configuration, and background jobs
- tests and code generation boundaries

For each major area, record its purpose and 1-3 representative files.

### 5. Extract Working Rules

- Infer install, dev, build, test, lint, and migration commands from manifests and scripts.
- Infer naming and structure conventions from the existing code, not from assumptions.
- Note generated code, migration flows, schema ownership, shared modules, and tightly coupled areas.
- Mention secret-bearing files only as configuration sources. Never surface actual secrets.

### 6. Produce the Orientation

- If the user asked for a conversational briefing, answer in chat using the reference template.
- If the user asked for persistent onboarding context, create or update `PROJECT_STRUCTURE.md` in the repository root.
- If `PROJECT_STRUCTURE.md` already exists, validate it against the codebase and update only stale or missing sections.

## Minimum Questions To Answer

Stop exploring once you can answer these with file-backed confidence:

- What does this repository do?
- How do you run, build, and test it?
- What are the main entry points and boot files?
- Where would a new change most likely belong?
- Which areas are shared, fragile, or risky to edit?

If one of these is still unclear, say so directly instead of guessing.

## Monorepo And Multi-Service Rules

- Separate the summary by app or service when the repository has more than one runnable target.
- Identify shared packages and cross-cutting infrastructure before drilling into individual apps.
- Do not collapse unrelated services into one summary just because they share a repository.

## Output Reference

When preparing the final briefing or a persistent note, read [references/orientation-template.md](references/orientation-template.md) and follow its structure. Fill only sections that can be justified from local files.
