@echo off
REM Build helper: freeze server.py into a standalone Windows exe (optional)
REM Requires: pip install pyinstaller
cd /d "%~dp0"
python -m PyInstaller --onefile --noconsole --name bishad-server server.py
echo Built dist\bishad-server.exe
pause
