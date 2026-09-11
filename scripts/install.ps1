# Antigravity Autopilot - One-Click Windows Installer
# Installs intelligent model routing, autonomous project mode, and CLI tools machine-wide.

[CmdletBinding()]
param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  ANTIGRAVITY AUTOPILOT - ONE-CLICK INSTALLER" -ForegroundColor Cyan
Write-Host "  (Experimental Tooling - Use At Your Own Risk)" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$configDir = Join-Path $HOME ".gemini\config"
$skillsDir = Join-Path $configDir "skills"
$binTarget = Join-Path $HOME ".gemini\antigravity\bin"

# 1. Verify / Create Directories
Write-Host "[1/5] Checking Antigravity environment..." -ForegroundColor Yellow
foreach ($dir in @($configDir, $skillsDir, $binTarget)) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Gray
    }
}

# 2. Install Global Orchestration Rules (AGENTS.md)
Write-Host "[2/5] Installing Global Orchestration Guidelines..." -ForegroundColor Yellow
$agentsSrc = Join-Path $root "customizations\rules\AGENTS.md"
$agentsDst = Join-Path $configDir "AGENTS.md"

if (Test-Path $agentsDst) {
    $existing = Get-Content $agentsDst -Raw -ErrorAction SilentlyContinue
    if ($existing -notlike "*Antigravity Global Model Orchestration Guidelines*") {
        Write-Host "  Existing AGENTS.md detected; merging guidelines..." -ForegroundColor Gray
        $merged = $existing + "`r`n`r`n" + (Get-Content $agentsSrc -Raw)
        Set-Content -Path $agentsDst -Value $merged -Encoding utf8
    } else {
        Write-Host "  Updating existing Antigravity orchestration rules..." -ForegroundColor Gray
        Copy-Item -Path $agentsSrc -Destination $agentsDst -Force
    }
} else {
    Copy-Item -Path $agentsSrc -Destination $agentsDst -Force
}
Write-Host "  Installed: $agentsDst" -ForegroundColor Green

# 3. Install Custom Skills
Write-Host "[3/5] Installing Global Skills (model-router, project-autopilot)..." -ForegroundColor Yellow
$skillsSrc = Join-Path $root "customizations\skills"

foreach ($skill in @("model-router", "project-autopilot")) {
    $srcFolder = Join-Path $skillsSrc $skill
    $dstFolder = Join-Path $skillsDir $skill
    if (!(Test-Path $dstFolder)) {
        New-Item -ItemType Directory -Path $dstFolder -Force | Out-Null
    }
    Copy-Item -Path "$srcFolder\*" -Destination $dstFolder -Recurse -Force
    Write-Host "  Installed Skill: $skill -> $dstFolder" -ForegroundColor Gray
}

# Register in skills.json
$skillsJsonPath = Join-Path $configDir "skills.json"
$skillsJsonObj = @{
    entries = @(
        @{ path = "skills" }
    )
}
$skillsJsonObj | ConvertTo-Json -Depth 3 | Set-Content -Path $skillsJsonPath -Encoding utf8
Write-Host "  Configured: $skillsJsonPath" -ForegroundColor Green

# 4. Install Binaries and CLI Tools
Write-Host "[4/5] Installing CLI Tools & Python Runners..." -ForegroundColor Yellow
$binSrc = Join-Path $root "bin"
Copy-Item -Path "$binSrc\*" -Destination $binTarget -Force

# Add to User PATH if missing
$userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$binTarget*") {
    [System.Environment]::SetEnvironmentVariable("Path", "$userPath;$binTarget", "User")
    Write-Host "  Added $binTarget to Windows User PATH" -ForegroundColor Green
} else {
    Write-Host "  PATH already configured." -ForegroundColor Gray
}

# 5. Verify Installation
Write-Host "[5/5] Running Self-Verification Test..." -ForegroundColor Yellow
$testOutput = & python (Join-Path $binTarget "agy_router.py") "Write unit test for user service"
if ($LASTEXITCODE -eq 0) {
    Write-Host "  Verification passed!" -ForegroundColor Green
} else {
    Write-Host "  Warning: Verification exited with code $LASTEXITCODE" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  INSTALLATION COMPLETED SUCCESSFULLY!" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Available CLI commands from any terminal:" -ForegroundColor White
Write-Host "  * agy-route <prompt>      : Classify and select optimal model" -ForegroundColor White
Write-Host "  * agy-autopilot --status  : Inspect current project settings" -ForegroundColor White
Write-Host "  * agy-autopilot --enable-autopilot : Enable autonomous permissions" -ForegroundColor White
Write-Host ""
