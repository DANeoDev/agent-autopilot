Write-Host "Uninstalling Antigravity Autopilot customizations..." -ForegroundColor Yellow

$configDir = Join-Path $HOME ".gemini\config"
$binDir = Join-Path $HOME ".gemini\antigravity\bin"

Remove-Item -Path (Join-Path $configDir "skills\model-router") -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path (Join-Path $configDir "skills\project-autopilot") -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path (Join-Path $binDir "agy_router.py") -Force -ErrorAction SilentlyContinue
Remove-Item -Path (Join-Path $binDir "agy-route.bat") -Force -ErrorAction SilentlyContinue
Remove-Item -Path (Join-Path $binDir "agy_project_manager.py") -Force -ErrorAction SilentlyContinue
Remove-Item -Path (Join-Path $binDir "agy-autopilot.bat") -Force -ErrorAction SilentlyContinue

Write-Host "Custom skills and binaries removed." -ForegroundColor Green
Write-Host "Note: ~/.gemini/config/AGENTS.md was preserved to prevent accidental loss of other rules." -ForegroundColor Cyan
