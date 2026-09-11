# Antigravity Autopilot - Universal Multi-Agent Terminal Installer
# Installs intelligent model routing, autonomous project mode, and CLI tools across:
# Google Antigravity, Anthropic Claude Code, Cursor, Windsurf, OpenAI Codex & Universal Agents.

[CmdletBinding()]
param(
    [string]$Target = "auto",   # "auto", "all", "antigravity", "claude", "cursor", "windsurf", "codex"
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  AUTOPILOT - UNIVERSAL MULTI-AGENT INSTALLER" -ForegroundColor Cyan
Write-Host "  Supporting: Antigravity, Claude Code, Cursor, Windsurf, Codex" -ForegroundColor White
Write-Host "  (Experimental Tooling - Use At Your Own Risk)" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$agentsSrc = Join-Path $root "customizations\rules\AGENTS.md"
$skillsSrc = Join-Path $root "customizations\skills"
$binSrc = Join-Path $root "bin"
$binTarget = Join-Path $HOME ".gemini\antigravity\bin"

function Install-AgentRules {
    param(
        [string]$TargetFile,
        [string]$SourceFile,
        [string]$AgentName
    )
    $dir = Split-Path -Parent $TargetFile
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    if (Test-Path $TargetFile) {
        $existing = Get-Content $TargetFile -Raw -ErrorAction SilentlyContinue
        if ($existing -notlike "*Antigravity Global Model Orchestration Guidelines*") {
            Write-Host "  [$AgentName] Existing config detected; appending Autopilot guidelines..." -ForegroundColor Gray
            $merged = $existing.TrimEnd() + "`r`n`r`n" + (Get-Content $SourceFile -Raw)
            Set-Content -Path $TargetFile -Value $merged -Encoding utf8
        } else {
            Write-Host "  [$AgentName] Updating existing Autopilot guidelines..." -ForegroundColor Gray
            Copy-Item -Path $SourceFile -Destination $TargetFile -Force
        }
    } else {
        Copy-Item -Path $SourceFile -Destination $TargetFile -Force
    }
    Write-Host "  [$AgentName] Installed: $TargetFile" -ForegroundColor Green
}

# 1. Target: Google Antigravity
if ($Target -in @("auto", "all", "antigravity")) {
    Write-Host "[1/6] Configuring Google Antigravity..." -ForegroundColor Yellow
    $configDir = Join-Path $HOME ".gemini\config"
    $skillsDir = Join-Path $configDir "skills"
    
    foreach ($dir in @($configDir, $skillsDir, $binTarget)) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
    }

    Install-AgentRules -TargetFile (Join-Path $configDir "AGENTS.md") -SourceFile $agentsSrc -AgentName "Antigravity"

    # Install custom skills
    foreach ($skill in @("model-router", "project-autopilot")) {
        $srcFolder = Join-Path $skillsSrc $skill
        $dstFolder = Join-Path $skillsDir $skill
        if (!(Test-Path $dstFolder)) {
            New-Item -ItemType Directory -Path $dstFolder -Force | Out-Null
        }
        Copy-Item -Path "$srcFolder\*" -Destination $dstFolder -Recurse -Force
        Write-Host "  [Antigravity] Installed Skill: $skill" -ForegroundColor Gray
    }

    # Register skills in skills.json
    $skillsJsonPath = Join-Path $configDir "skills.json"
    $skillsJsonObj = @{ entries = @(@{ path = "skills" }) }
    $skillsJsonObj | ConvertTo-Json -Depth 3 | Set-Content -Path $skillsJsonPath -Encoding utf8
}

# 2. Target: Anthropic Claude Code (claude)
$claudeDir = Join-Path $HOME ".claude"
if ($Target -in @("all", "claude") -or ($Target -eq "auto" -and (Test-Path $claudeDir))) {
    Write-Host "[2/6] Configuring Anthropic Claude Code..." -ForegroundColor Yellow
    Install-AgentRules -TargetFile (Join-Path $claudeDir "CLAUDE.md") -SourceFile $agentsSrc -AgentName "Claude Code"
}

# 3. Target: Cursor AI Agent
$cursorDir = Join-Path $HOME ".cursor"
$cursorApp = Join-Path $HOME "AppData\Roaming\Cursor"
if ($Target -in @("all", "cursor") -or ($Target -eq "auto" -and ((Test-Path $cursorDir) -or (Test-Path $cursorApp)))) {
    Write-Host "[3/6] Configuring Cursor AI Agent..." -ForegroundColor Yellow
    Install-AgentRules -TargetFile (Join-Path $HOME ".cursorrules") -SourceFile $agentsSrc -AgentName "Cursor"
}

# 4. Target: Windsurf Cascade
$codeiumDir = Join-Path $HOME ".codeium"
$windsurfDir = Join-Path $HOME ".windsurf"
if ($Target -in @("all", "windsurf") -or ($Target -eq "auto" -and ((Test-Path $codeiumDir) -or (Test-Path $windsurfDir)))) {
    Write-Host "[4/6] Configuring Windsurf Cascade..." -ForegroundColor Yellow
    Install-AgentRules -TargetFile (Join-Path $HOME ".windsurfrules") -SourceFile $agentsSrc -AgentName "Windsurf"
}

# 5. Target: Universal Agent Standard & OpenAI Codex
if ($Target -in @("auto", "all", "codex", "universal")) {
    Write-Host "[5/6] Configuring Universal Agent Standards (Codex, Aider, OpenHands)..." -ForegroundColor Yellow
    Install-AgentRules -TargetFile (Join-Path $HOME "AGENTS.md") -SourceFile $agentsSrc -AgentName "Universal Home"
    $agentsConfigDir = Join-Path $HOME ".config\agents"
    Install-AgentRules -TargetFile (Join-Path $agentsConfigDir "AGENTS.md") -SourceFile $agentsSrc -AgentName "Universal Config"
}

# 6. Install Global Binaries & CLI Tools to User PATH
Write-Host "[6/6] Installing CLI Tools & Configuring PATH..." -ForegroundColor Yellow
if (!(Test-Path $binTarget)) {
    New-Item -ItemType Directory -Path $binTarget -Force | Out-Null
}
Copy-Item -Path "$binSrc\*" -Destination $binTarget -Force

$userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$binTarget*") {
    [System.Environment]::SetEnvironmentVariable("Path", "$userPath;$binTarget", "User")
    Write-Host "  Added $binTarget to Windows User PATH" -ForegroundColor Green
} else {
    Write-Host "  PATH already configured." -ForegroundColor Gray
}

# Self-Verification Test
Write-Host "Running Self-Verification Test..." -ForegroundColor Yellow
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
Write-Host "Available CLI commands across all agent terminals:" -ForegroundColor White
Write-Host "  * agy-route / agent-route         : Classify and select optimal model" -ForegroundColor White
Write-Host "  * agy-autopilot / agent-autopilot : Inspect or enable autonomous mode" -ForegroundColor White
Write-Host "  * agy-predict / agent-predict     : Predict continuous complex pass depth (Z = X + iY)" -ForegroundColor White
Write-Host ""

