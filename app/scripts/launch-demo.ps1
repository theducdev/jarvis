# JARVIS demo launcher — starts backend, frontend, and clap listener in separate windows.
$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$AppDir = Join-Path $ProjectRoot 'app'

Write-Host '==> Starting JARVIS backend (FastAPI :8000)...' -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    '-NoExit', '-Command',
    "cd `"$AppDir\backend`"; venv\Scripts\Activate.ps1; uvicorn src.main:app --host 0.0.0.0 --port 8000"
) -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host '==> Starting frontend (Vite :3000)...' -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    '-NoExit', '-Command',
    "cd `"$AppDir\frontend`"; npm run dev"
) -WindowStyle Normal

Start-Sleep -Seconds 4

Write-Host '==> Starting clap-wake listener...' -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    '-NoExit', '-Command',
    "cd `"$AppDir`"; backend\venv\Scripts\python.exe clap-wake-listener.py"
) -WindowStyle Normal

Start-Sleep -Seconds 2
Start-Process 'http://localhost:3000'

Write-Host ''
Write-Host 'JARVIS demo is running.' -ForegroundColor Green
Write-Host '  Backend  : http://localhost:8000/docs' -ForegroundColor Gray
Write-Host '  Frontend : http://localhost:3000' -ForegroundColor Gray
Write-Host '  Wake     : clap your hands twice' -ForegroundColor Gray
Write-Host ''
Write-Host "Stop everything: .\scripts\stop-demo.ps1" -ForegroundColor Yellow
