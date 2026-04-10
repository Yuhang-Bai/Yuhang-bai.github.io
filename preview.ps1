$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not available in PATH." -ForegroundColor Red
    exit 1
}

Set-Location $scriptDir
python preview.py
