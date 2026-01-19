# AI Agent Config Installer for Windows
# Supports: Claude Code, OpenAI Codex
# Usage: Run in PowerShell (Administrator recommended for symlinks)
#
# 경로 자동 탐색 후 연결합니다. 찾지 못하면 수동 입력을 받습니다.

$ErrorActionPreference = "Stop"

$REPO = "https://github.com/testkim00/ai-agent-config.git"
$CONFIG_DIR = "$env:USERPROFILE\.ai-agent-config"

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

# Function to find directory from multiple candidates
function Find-AgentDir {
    param (
        [string]$AgentName,
        [string[]]$Candidates
    )

    foreach ($path in $Candidates) {
        $expanded = [Environment]::ExpandEnvironmentVariables($path)
        if (Test-Path $expanded) {
            Write-Host "  Found $AgentName at: $expanded" -ForegroundColor Green
            return $expanded
        }
    }

    # Not found - ask user
    Write-Host "  $AgentName directory not found in default locations." -ForegroundColor Yellow
    Write-Host "  Searched:" -ForegroundColor Gray
    foreach ($path in $Candidates) {
        Write-Host "    - $path" -ForegroundColor Gray
    }

    $userPath = Read-Host "  Enter $AgentName directory path (or press Enter to skip)"
    if ($userPath -and (Test-Path $userPath)) {
        return $userPath
    }

    return $null
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

# ============================================================
# Claude Code Setup
# ============================================================
Write-Host "`n[Claude Code]" -ForegroundColor Cyan

$CLAUDE_CANDIDATES = @(
    "$env:USERPROFILE\.claude",
    "$env:APPDATA\claude",
    "$env:LOCALAPPDATA\claude",
    "$env:APPDATA\Claude",
    "$env:LOCALAPPDATA\Claude",
    "$env:USERPROFILE\AppData\Roaming\claude",
    "$env:USERPROFILE\AppData\Local\claude"
)

$CLAUDE_DIR = Find-AgentDir -AgentName "Claude Code" -Candidates $CLAUDE_CANDIDATES

if ($CLAUDE_DIR) {
    New-ConfigLink -LinkPath "$CLAUDE_DIR\skills" -TargetPath "$CONFIG_DIR\claude\skills" -Name "skills"
    New-ConfigLink -LinkPath "$CLAUDE_DIR\commands" -TargetPath "$CONFIG_DIR\claude\commands" -Name "commands"
    New-ConfigLink -LinkPath "$CLAUDE_DIR\Claude.md" -TargetPath "$CONFIG_DIR\claude\CLAUDE.md" -Name "Claude.md"
    Write-Host "  Claude Code configured" -ForegroundColor Green
} else {
    Write-Host "  Skipped." -ForegroundColor Yellow
}

# ============================================================
# Codex Setup
# ============================================================
Write-Host "`n[Codex]" -ForegroundColor Cyan

$CODEX_CANDIDATES = @(
    "$env:USERPROFILE\.codex",
    "$env:APPDATA\codex",
    "$env:LOCALAPPDATA\codex",
    "$env:APPDATA\Codex",
    "$env:LOCALAPPDATA\Codex",
    "$env:USERPROFILE\AppData\Roaming\codex",
    "$env:USERPROFILE\AppData\Local\codex"
)

$CODEX_DIR = Find-AgentDir -AgentName "Codex" -Candidates $CODEX_CANDIDATES

if ($CODEX_DIR) {
    New-ConfigLink -LinkPath "$CODEX_DIR\skills" -TargetPath "$CONFIG_DIR\codex\skills" -Name "skills"
    Write-Host "  Codex configured" -ForegroundColor Green
} else {
    Write-Host "  Skipped." -ForegroundColor Yellow
}

# ============================================================
# Done
# ============================================================
Write-Host "`n=== Installation Complete ===" -ForegroundColor Cyan
Write-Host "Config location: $CONFIG_DIR"
Write-Host ""
Write-Host "Commands:"
Write-Host "  Sync:  $CONFIG_DIR\sync.ps1"
Write-Host "  Push:  $CONFIG_DIR\push.ps1"
