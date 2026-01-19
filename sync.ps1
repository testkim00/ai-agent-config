# Sync config from remote (Windows)

$ErrorActionPreference = "Stop"

$CONFIG_DIR = "$env:USERPROFILE\.ai-agent-config"

if (-not (Test-Path $CONFIG_DIR)) {
    Write-Host "Error: Config not installed. Run install.ps1 first." -ForegroundColor Red
    exit 1
}

Push-Location $CONFIG_DIR

# Check for local changes
$status = git status --porcelain
if ($status) {
    Write-Host "Warning: Local changes detected." -ForegroundColor Yellow
    Write-Host "  - Stash: git stash"
    Write-Host "  - Discard: git checkout ."
    Write-Host ""
    $reply = Read-Host "Discard local changes and sync? (y/N)"
    if ($reply -eq 'y' -or $reply -eq 'Y') {
        git checkout .
    } else {
        Write-Host "Sync cancelled."
        Pop-Location
        exit 1
    }
}

Write-Host "Syncing from remote..."
git pull

Pop-Location

Write-Host "Sync complete" -ForegroundColor Green
