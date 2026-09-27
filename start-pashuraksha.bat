@echo off

 powershell -NoProfile -Command "if (Get-NetTCPConnection -State Listen -LocalPort 8000 -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }"
if errorlevel 1 (
	cd /d "C:\Users\chandrika\Documents\PashuRaksha\backend"
	start "PashuRaksha Backend" cmd /k ".\venv\Scripts\python.exe -m uvicorn main:app --reload"
	timeout /t 3 /nobreak >nul
)

powershell -NoProfile -Command "if (Get-NetTCPConnection -State Listen -LocalPort 5175 -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }"
if errorlevel 1 (
	cd /d "C:\Users\chandrika\Documents\PashuRaksha\frontend"
	start "PashuRaksha Frontend" cmd /k "npm run dev"
	timeout /t 5 /nobreak >nul
)

start http://localhost:5175
@echo off
title PashuRaksha

echo ==========================================
echo          PASHURAKSHA STARTING
echo ==========================================
echo.

echo Starting Backend...
start "PashuRaksha Backend" cmd /k "cd /d C:\Users\chandrika\Documents\PashuRaksha\backend && .\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo Starting Frontend...
start "PashuRaksha Frontend" cmd /k "cd /d C:\Users\chandrika\Documents\PashuRaksha\frontend && npm run dev -- --host localhost --port 5173"

timeout /t 6 /nobreak >nul

echo Opening PashuRaksha...
start http://localhost:5173

echo.
echo PashuRaksha is running.
