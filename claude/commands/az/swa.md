---
name: manage-azure-swa
description: "Manage Azure Static Web Apps: inventory, deployment, custom domains, SSL, RBAC. Use WHEN deploying to SWA, WHEN checking SWA status, WHEN managing SWA domains/SSL, WHEN granting SWA permissions, WHEN syncing SWA inventory. NOT for App Service (use /az:web-app), NOT for APIM (use /az:apim)."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash(az:*), Bash(swa:*), Bash(npm:*), Bash(curl:*), Bash(dig:*), Bash(git:*), AskUserQuestion, mcp__azure__role, mcp__azure__group_list]
---

# Manage Azure SWA

SWA lifecycle management: inventory cache, deployment (SWA CLI), custom domains, SSL, RBAC.

## INTENT_ROUTER

| Intent | Keywords | Workflow |
|--------|----------|----------|
| INVENTORY | list, show, sync, env, status | WORKFLOW_INVENTORY |
| DEPLOY | deploy, push, upload | WORKFLOW_DEPLOY |
| DOMAIN | domain, ssl, hostname, certificate | WORKFLOW_DOMAIN |
| RBAC | permission, role, access, grant | WORKFLOW_RBAC |

---

## INVENTORY

Cached SWA resource map: [references/swa-inventory.json](references/swa-inventory.json)

### Structure

```json
{
  "last_synced": "ISO timestamp",
  "resource_groups": {
    "<rg-name>": {
      "<swa-name>": {
        "sku": "Free|Standard",
        "defaultHostname": "*.azurestaticapps.net",
        "customDomains": [],
        "project": "local path (from github-env.json local_mapping)",
        "repo": "GitHub repo name",
        "buildOutput": "dist/spa or dist/pwa",
        "purpose": "production|testbed"
      }
    }
  }
}
```

### WORKFLOW_INVENTORY

```
1. Read references/swa-inventory.json (cached)

2. IF sync requested OR cache older than 7 days:
   az staticwebapp list --query "[].{name:name, rg:resourceGroup, sku:sku.name, host:defaultHostname}" -o json
   FOR each SWA:
     az staticwebapp hostname list --name <name> --query "[].domainName" -o tsv
   Cross-reference with github-env.json local_mapping
   Update references/swa-inventory.json

3. Display inventory table:
   | SWA Resource | SKU | Project | Custom Domain | Purpose |
```

---

## WORKFLOW_DEPLOY

### Pre-flight

```
1. Check SWA CLI: swa --version
2. Read swa-cli.config.json in project root
   - configurations 객체에서 첫 번째 (또는 유일한) config name 자동 감지
   - config name이 1개면 그대로 사용, 2개 이상이면 사용자에게 선택 요청
3. Resolve: appName, resourceGroup, outputLocation from detected config
```

### Deploy (default)

```
1. Confirm target: "Deploying to {appName} ({resourceGroup})"
2. Build (user choice):
   - AskUserQuestion: "빌드 방식을 선택하세요"
     (1) build (SPA)  (2) build:pwa (PWA)  (3) 이미 빌드됨 (skip)
   - Execute chosen build command
3. Deploy:
   swa deploy --config-name <auto-detected-config-name> --env production
   ⚠️ --env production REQUIRED! Default is preview environment (custom domains not applied)
4. Post-deploy: git checkout .env (SWA CLI writes Azure credentials to .env; restore after deploy)
5. Verify:
   curl -sI https://<default-hostname>
   Check HTTP/2 200, Cache-Control headers
```

### Production 명시 배포 (사용자가 "운영" 또는 "production" 명시 시)

```
1. ⚠️ WARNING block:
   "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ⚠️  PRODUCTION DEPLOY WARNING
    Target: {appName} ({resourceGroup})
    This action takes effect on live service immediately.
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

2. AskUserQuestion: "운영 배포를 진행할까요? (yes 입력)"
   IF answer != "yes": abort

3. Build + Deploy: same as default flow
```

### swa-cli.config.json 없는 경우 (fallback)

```
TOKEN=$(az staticwebapp secrets list --name <swa-name> --query "properties.apiKey" -o tsv)
swa deploy <output-dir> --deployment-token $TOKEN --env production
```

---

## WORKFLOW_DOMAIN

### List Domains

```
az staticwebapp hostname list --name <swa-name> -o table
```

### Register Custom Domain

```
1. Verify DNS CNAME:
   dig +short <hostname> CNAME
   Expected: <swa-default-hostname>.

2. Register:
   az staticwebapp hostname set --name <swa-name> --hostname <hostname>
   (blocks until validation + SSL certificate issued)

3. Verify SSL:
   curl -v https://<hostname> 2>&1 | grep -E "SSL|subject|issuer|certificate"
```

### Check SSL Status

```
az staticwebapp hostname list --name <swa-name> --query "[].{domain:domainName, status:status}" -o table
```

---

## WORKFLOW_RBAC

### List Assignments

```
SCOPE="/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Web/staticSites/<swa-name>"
mcp__azure__role(command: "role_assignment_list", parameters: {scope: SCOPE, subscription: <sub>})
```

### Grant Access

```
1. Identify principalId:
   az ad user show --id <email> --query "id" -o tsv

2. Assign role:
   az role assignment create \
     --assignee <principalId> \
     --role "Contributor" \
     --scope "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Web/staticSites/<swa-name>"

3. Confirm: "Granted {user} Contributor role on {swa-name}"
```

**Scope note**: `Microsoft.Web/staticSites` ≠ `Microsoft.Web/sites`. App Service RBAC does NOT apply to SWA.

---

## CONVENTIONS

- SWA resource naming: `swa-{app}-client` (production), `swa-{app}-client-testbed` (testbed)
- swa-cli.config.json: `appBuildCommand: ""` (separate build/deploy), `appName` + `resourceGroup` required (prevents interactive prompt)
- GitHub Actions workflow naming: `{default-branch}_swa_{app}.yml`
- GitHub Secret: `AZURE_STATIC_WEB_APPS_API_TOKEN`
- staticwebapp.config.json: located at project root, `globalHeaders: no-cache` inversion strategy required

---

## CONSTRAINTS

- Use SWA CLI (`swa deploy`) — `az staticwebapp deploy` command does NOT exist
- **`--env production` REQUIRED**: `swa deploy` defaults to `preview` environment. Custom domains bind to production only
- **`.env` write-back caution**: `swa login`/`swa deploy` writes Azure credentials to project `.env`. If `.env` is git-tracked, run `git checkout .env` after deploy
- **`staticwebapp.config.json` auto-included**: SWA CLI auto-detects config at `appLocation` root — no manual copy needed. Only GitHub Actions (`skip_app_build: true`) requires explicit copy step
- VS Code SWA Extension: resource management only, no deploy capability (requires GitHub Actions)
- Azure Portal: no direct file upload UI
- SWA Free tier: includes custom domain + SSL, no PR Preview (auth constraint)
- Deployment token: unique per SWA resource

---

## ERROR_HANDLING

| Error | Action |
|-------|--------|
| `swa --version` fails | Suggest `npm install -g @azure/static-web-apps-cli` |
| `swa deploy` auth failure | Use `swa login` or `--deployment-token` |
| DNS CNAME mismatch | Compare `dig +short` result with SWA defaultHostname, suggest DNS fix |
| SSL "Adding" status persists | Azure Managed Certificate issuance up to 10min, suggest polling |
| `staticwebapp.config.json` not applied | SWA CLI auto-includes from `appLocation`. GitHub Actions (`skip_app_build: true`) requires copy to `dist/` |

---

**Version**: 1.1.0
**Created**: 2026-03-11
