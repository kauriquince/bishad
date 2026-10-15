@echo off
REM Tabitha & Bishad v3 — PC auto-start wrapper (Windows)
setlocal EnableDelayedExpansion
cd /d "%~dp0"

set "OLLAMA_URL=http://127.0.0.1:11434"
set "SERVER_URL=http://127.0.0.1:8765"

echo [bishad] checking Ollama...
curl -s -o nul -w "%%{http_code}" %OLLAMA_URL%/api/tags > %TEMP%\bishad_ollama_code.txt 2>nul
set /p CODE= < %TEMP%\bishad_ollama_code.txt
del %TEMP%\bishad_ollama_code.txt >nul 2>&1

if not "!CODE!"=="200" (
  echo [bishad] Ollama not responding - starting it...
  start "" /B ollama serve
  echo [bishad] waiting for API...
  set /a TRY=0
  :wait
  timeout /t 2 /nobreak >nul
  curl -s -o nul -w "%%{http_code}" %OLLAMA_URL%/api/tags > %TEMP%\bishad_ollama_code.txt 2>nul
  set /p CODE= < %TEMP%\bishad_ollama_code.txt
  del %TEMP%\bishad_ollama_code.txt >nul 2>&1
  set /a TRY+=1
  if not "!CODE!"=="200" if !TRY! lss 30 goto wait
  if not "!CODE!"=="200" (
    echo [bishad] ERROR: Ollama did not start. Is it installed? Check PATH.
    pause
    exit /b 1
  )
  echo [bishad] Ollama is up.
) else (
  echo [bishad] Ollama already running.
)

echo [bishad] starting server...
start "Tabitha and Bishad" cmd /k python server.py
echo [bishad] opening browser...
start "" %SERVER_URL%
echo [bishad] done. Close the server window to stop.
pause
