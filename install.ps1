# AI Agent Config Installer for Windows
# Supports: Claude Code, OpenAI Codex
# Usage: Run in PowerShell (Administrator recommended for symlinks)

$ErrorActionPreference = "Stop"

$REPO = "https://github.com/testkim00/ai-agent-config.git"
$CONFIG_DIR = "$env:USERPROFILE\.ai-agent-config"
$CLAUDE_DIR = "$env:USERPROFILE\.claude"
$CODEX_DIR = "$env:USERPROFILE\.codex"

Write-Host "=== AI Agent Config Installer ===" -ForegroundColor Cyan

# Clone or update
if (Test-Path $CONFIG_DIR) {
    Write-Host "Updating existing config..."
    Push-Location $CONFIG_DIR
    git pull
    Pop-Location
} else {
    Write-Host "Cloning config repository..."
    git clone $REPO $CONFIG_DIR
}

# Function to create symlink with fallback to copy
function New-ConfigLink {
    param (
        [string]$LinkPath,
        [string]$TargetPath,
        [string]$Name
    )

    # Backup existing (if not already a symlink)
    if (Test-Path $LinkPath) {
        $item = Get-Item $LinkPath
        if (-not $item.Attributes.ToString().Contains("ReparsePoint")) {
            $backupPath = "$LinkPath.bak"
            Write-Host "  Backing up existing $Name to $backupPath"
            if (Test-Path $backupPath) { Remove-Item -Recurse -Force $backupPath }
            Move-Item $LinkPath $backupPath
        } else {
            # Remove existing symlink
            Remove-Item $LinkPath -Force
        }
    }

    # Try to create symlink
    try {
        New-Item -ItemType SymbolicLink -Path $LinkPath -Target $TargetPath -Force | Out-Null
        Write-Host "  [Symlink] $Name" -ForegroundColor Green
    } catch {
        # Fallback: use junction for directories
        Write-Host "  [Junction] $Name (symlink failed, using junction)" -ForegroundColor Yellow
        cmd /c mklink /J "$LinkPath" "$TargetPath" 2>$null
        if (-not $?) {
            # Final fallback: copy files
            Write-Host "  [Copy] $Name (junction failed, copying files)" -ForegroundColor Yellow
            Copy-Item -Path $TargetPath -Destination $LinkPath -Recurse -Force
        }
    }
}

# Claude Code setup
if (Test-Path $CLAUDE_DIR) {
    Write-Host "`nSetting up Claude Code..."

    New-ConfigLink -LinkPath "$CLAUDE_DIR\skills" -TargetPath "$CONFIG_DIR\claude\skills" -Name "skills"
    New-ConfigLink -LinkPath "$CLAUDE_DIR\commands" -TargetPath "$CONFIG_DIR\claude\commands" -Name "commands"

    Write-Host "  Claude Code configured" -ForegroundColor Green
} else {
    Write-Host "`nClaude Code directory not found. Skipping..." -ForegroundColor Yellow
}

# Codex setup
if (Test-Path $CODEX_DIR) {
    Write-Host "`nSetting up Codex..."

    New-ConfigLink -LinkPath "$CODEX_DIR\skills" -TargetPath "$CONFIG_DIR\codex\skills" -Name "skills"

    Write-Host "  Codex configured" -ForegroundColor Green
} else {
    Write-Host "`nCodex directory not found. Skipping..." -ForegroundColor Yellow
}

Write-Host "`n=== Installation Complete ===" -ForegroundColor Cyan
Write-Host "Config location: $CONFIG_DIR"
Write-Host ""
Write-Host "Commands:"
Write-Host "  Sync:  $CONFIG_DIR\sync.ps1"
Write-Host "  Push:  $CONFIG_DIR\push.ps1"
