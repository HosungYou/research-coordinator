# =============================================================================
# Research Coordinator - Windows Installation Script
# =============================================================================
# PowerShell installation script for Windows users
#
# Usage:
#   .\scripts\install.ps1              # Install with symlinks (default)
#   .\scripts\install.ps1 -Copy        # Install by copying files
#   .\scripts\install.ps1 -Uninstall   # Remove installation
#
# Requirements:
#   - PowerShell 5.1 or later
#   - Administrator privileges (for symlinks) or use -Copy flag
#
# Author: Research Coordinator v3.1
# License: MIT
# =============================================================================

param(
    [switch]$Copy,
    [switch]$Uninstall,
    [switch]$Help
)

# Colors
$Green = "Green"
$Red = "Red"
$Yellow = "Yellow"
$Cyan = "Cyan"

function Write-Success { param($msg) Write-Host "✓ $msg" -ForegroundColor $Green }
function Write-Error { param($msg) Write-Host "✗ $msg" -ForegroundColor $Red }
function Write-Warning { param($msg) Write-Host "! $msg" -ForegroundColor $Yellow }
function Write-Info { param($msg) Write-Host "ℹ $msg" -ForegroundColor $Cyan }

function Show-Banner {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════╗" -ForegroundColor $Cyan
    Write-Host "║         Research Coordinator Installer v3.1           ║" -ForegroundColor $Cyan
    Write-Host "║    사회과학 연구자를 위한 AI 에이전트 시스템           ║" -ForegroundColor $Cyan
    Write-Host "╚═══════════════════════════════════════════════════════╝" -ForegroundColor $Cyan
    Write-Host ""
}

function Show-Help {
    Show-Banner
    Write-Host "Usage: .\scripts\install.ps1 [options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Copy       Install by copying files (no admin required)"
    Write-Host "  -Uninstall  Remove Research Coordinator installation"
    Write-Host "  -Help       Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\scripts\install.ps1           # Install with symlinks"
    Write-Host "  .\scripts\install.ps1 -Copy     # Install by copying"
    Write-Host "  .\scripts\install.ps1 -Uninstall"
    Write-Host ""
}

function Test-Admin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Install-ResearchCoordinator {
    param([bool]$UseCopy)

    Show-Banner
    Write-Host "Installing Research Coordinator..."
    Write-Host "───────────────────────────────────────────────────────"
    Write-Host ""

    # Paths
    $ScriptDir = Split-Path -Parent $MyInvocation.ScriptName
    $RepoDir = Split-Path -Parent $ScriptDir
    $SkillsDir = Join-Path $env:USERPROFILE ".claude\skills"
    $AgentsSource = Join-Path $RepoDir ".claude\skills\research-agents"
    $CoordinatorSource = Join-Path $RepoDir ".claude\skills\research-coordinator"
    $AgentsTarget = Join-Path $SkillsDir "research-agents"
    $CoordinatorTarget = Join-Path $SkillsDir "research-coordinator"

    # Check source directories exist
    if (-not (Test-Path $AgentsSource)) {
        Write-Error "Source directory not found: $AgentsSource"
        Write-Host "Please run this script from the repository root."
        exit 1
    }

    # Create skills directory
    if (-not (Test-Path $SkillsDir)) {
        Write-Info "Creating skills directory: $SkillsDir"
        New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
    }

    # Remove existing installations
    if (Test-Path $CoordinatorTarget) {
        Write-Info "Removing existing coordinator installation..."
        Remove-Item -Path $CoordinatorTarget -Recurse -Force
    }
    if (Test-Path $AgentsTarget) {
        Write-Info "Removing existing agents installation..."
        Remove-Item -Path $AgentsTarget -Recurse -Force
    }

    # Install
    if ($UseCopy) {
        Write-Info "Installing by copying files..."

        Copy-Item -Path $CoordinatorSource -Destination $CoordinatorTarget -Recurse -Force
        Write-Success "Copied research-coordinator"

        Copy-Item -Path $AgentsSource -Destination $AgentsTarget -Recurse -Force
        Write-Success "Copied research-agents"
    }
    else {
        # Check for admin privileges for symlinks
        if (-not (Test-Admin)) {
            Write-Warning "Creating symlinks requires Administrator privileges."
            Write-Warning "Run PowerShell as Administrator, or use -Copy flag."
            Write-Host ""
            Write-Host "Alternatives:"
            Write-Host "  1. Run as Administrator: Right-click PowerShell -> Run as Administrator"
            Write-Host "  2. Use copy mode: .\scripts\install.ps1 -Copy"
            exit 1
        }

        Write-Info "Creating symbolic links..."

        New-Item -ItemType SymbolicLink -Path $CoordinatorTarget -Target $CoordinatorSource | Out-Null
        Write-Success "Created symlink: research-coordinator -> $CoordinatorSource"

        New-Item -ItemType SymbolicLink -Path $AgentsTarget -Target $AgentsSource | Out-Null
        Write-Success "Created symlink: research-agents -> $AgentsSource"
    }

    # Count agents
    $AgentCount = (Get-ChildItem -Path $AgentsTarget -Directory).Count

    # Summary
    Write-Host ""
    Write-Host "───────────────────────────────────────────────────────"
    Write-Success "Installation complete!"
    Write-Host ""
    Write-Host "Installed:"
    Write-Host "  • Research Coordinator (master skill)"
    Write-Host "  • $AgentCount research agents"
    Write-Host ""
    Write-Host "Location: $SkillsDir"
    Write-Host ""
    Write-Host "Usage in Claude Code:"
    Write-Host "  /research-coordinator           # Start coordinator"
    Write-Host "  /research-question-refiner      # Call specific agent"
    Write-Host ""
    Write-Host "CLI Tool:"
    Write-Host "  python scripts\rc.py help       # Show available commands"
    Write-Host ""
}

function Uninstall-ResearchCoordinator {
    Show-Banner
    Write-Host "Uninstalling Research Coordinator..."
    Write-Host "───────────────────────────────────────────────────────"
    Write-Host ""

    $SkillsDir = Join-Path $env:USERPROFILE ".claude\skills"
    $CoordinatorTarget = Join-Path $SkillsDir "research-coordinator"
    $AgentsTarget = Join-Path $SkillsDir "research-agents"

    $removed = $false

    if (Test-Path $CoordinatorTarget) {
        Remove-Item -Path $CoordinatorTarget -Recurse -Force
        Write-Success "Removed research-coordinator"
        $removed = $true
    }

    if (Test-Path $AgentsTarget) {
        Remove-Item -Path $AgentsTarget -Recurse -Force
        Write-Success "Removed research-agents"
        $removed = $true
    }

    if ($removed) {
        Write-Host ""
        Write-Success "Uninstallation complete!"
    }
    else {
        Write-Warning "Nothing to uninstall - Research Coordinator was not installed."
    }
}

# Main
if ($Help) {
    Show-Help
    exit 0
}

if ($Uninstall) {
    Uninstall-ResearchCoordinator
    exit 0
}

Install-ResearchCoordinator -UseCopy:$Copy
