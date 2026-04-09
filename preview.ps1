$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not available in PATH." -ForegroundColor Red
    exit 1
}

Set-Location $scriptDir
python build_site.py

Write-Host ""
Write-Host "Preview server running at http://127.0.0.1:4000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""

python -m http.server 4000 --bind 127.0.0.1
