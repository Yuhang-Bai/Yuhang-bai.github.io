@echo off
cd /d "%~dp0"
python build_site.py
echo.
echo Preview server running at http://127.0.0.1:4000
echo Press Ctrl+C to stop.
echo.
python -m http.server 4000 --bind 127.0.0.1
