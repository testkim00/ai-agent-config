# Push local config changes to remote (Windows)

$ErrorActionPreference = "Stop"

$CONFIG_DIR = "$env:USERPROFILE\.ai-agent-config"

if (-not (Test-Path $CONFIG_DIR)) {
    Write-Host "Error: Config not installed. Run install.ps1 first." -ForegroundColor Red
    exit 1
}

Push-Location $CONFIG_DIR

# Check for changes
$status = git status --porcelain
if (-not $status) {
    Write-Host "No changes to push."
    Pop-Location
    exit 0
}

Write-Host "Changes:"
git status --short
Write-Host ""

$msg = Read-Host "Commit message"
if (-not $msg) {
    $msg = "config: update"
}

git add -A
git commit -m $msg
git push

Pop-Location

Write-Host "Push complete" -ForegroundColor Green
