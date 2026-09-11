Write-Host "Running Antigravity Autopilot Health Check..." -ForegroundColor Cyan

$configDir = Join-Path $HOME ".gemini\config"
$binDir = Join-Path $HOME ".gemini\antigravity\bin"

$checks = @(
    @{ Name = "Global Rules (AGENTS.md)"; Path = Join-Path $configDir "AGENTS.md" },
    @{ Name = "Skill: model-router"; Path = Join-Path $configDir "skills\model-router\SKILL.md" },
    @{ Name = "Skill: project-autopilot"; Path = Join-Path $configDir "skills\project-autopilot\SKILL.md" },
    @{ Name = "Router Binary"; Path = Join-Path $binDir "agy_router.py" },
    @{ Name = "Project Manager Binary"; Path = Join-Path $binDir "agy_project_manager.py" },
    @{ Name = "Cognitive Engine Binary"; Path = Join-Path $binDir "cognitive_engine.py" },
    @{ Name = "CLI Launcher (agy-route)"; Path = Join-Path $binDir "agy-route.bat" },
    @{ Name = "CLI Launcher (agy-autopilot)"; Path = Join-Path $binDir "agy-autopilot.bat" },
    @{ Name = "CLI Launcher (agy-predict)"; Path = Join-Path $binDir "agy-predict.bat" },
    @{ Name = "Universal Launcher (agent-route)"; Path = Join-Path $binDir "agent-route.bat" },
    @{ Name = "Universal Launcher (agent-autopilot)"; Path = Join-Path $binDir "agent-autopilot.bat" },
    @{ Name = "Universal Launcher (agent-predict)"; Path = Join-Path $binDir "agent-predict.bat" }
)


$allPassed = $true
foreach ($c in $checks) {
    if (Test-Path $c.Path) {
        Write-Host "  [OK] $($c.Name)" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] Missing: $($c.Path)" -ForegroundColor Red
        $allPassed = $false
    }
}

if ($allPassed) {
    Write-Host "`nAll components are verified and operational!" -ForegroundColor Green
} else {
    Write-Host "`nSome components were missing. Please re-run install.ps1" -ForegroundColor Yellow
}
