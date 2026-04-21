# Kill JARVIS demo processes.
Write-Host '==> Stopping JARVIS demo...' -ForegroundColor Yellow

# Kill by port (backend :8000, frontend :3000/5173)
foreach ($port in 8000, 3000, 5173) {
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    foreach ($c in $conns) {
        try {
            Stop-Process -Id $c.OwningProcess -Force -ErrorAction SilentlyContinue
            Write-Host "  killed pid=$($c.OwningProcess) on port $port" -ForegroundColor Gray
        } catch {}
    }
}

# Kill clap listener (python process running clap-wake-listener.py)
Get-WmiObject Win32_Process -Filter "Name = 'python.exe'" | ForEach-Object {
    if ($_.CommandLine -and $_.CommandLine -match 'clap-wake-listener') {
        try {
            Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
            Write-Host "  killed clap listener pid=$($_.ProcessId)" -ForegroundColor Gray
        } catch {}
    }
}

Write-Host 'Done.' -ForegroundColor Green
