@echo off
:: ============================================================
::  WellnessMitra — Start Application
::  Starts both Backend (FastAPI) + Frontend (React)
::  Double-click to launch the full app
:: ============================================================

title WellnessMitra — Starting...
set PATH=C:\Program Files\nodejs;%PATH%

echo.
echo  ========================================================
echo   WellnessMitra - AI Fitness ^& Wellness Agent
echo   Starting application...
echo  ========================================================
echo.

:: ── Check .env exists ─────────────────────────────────────────────────────────
if not exist ".env" (
    echo  ERROR: .env file not found!
    echo  Please run setup.bat first.
    pause
    exit /b 1
)

:: ── Check venv exists ─────────────────────────────────────────────────────────
if not exist "venv" (
    echo  ERROR: Virtual environment not found!
    echo  Please run setup.bat first.
    pause
    exit /b 1
)

:: ── Start Backend in new window ───────────────────────────────────────────────
echo  Starting Backend (FastAPI)...
start "WellnessMitra Backend" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && echo Backend starting on http://localhost:8000 && echo API Docs: http://localhost:8000/docs && uvicorn backend.api.main:app --reload --port 8000 --host 0.0.0.0"

:: ── Wait for backend to start ─────────────────────────────────────────────────
echo  Waiting for backend to initialize (10 seconds)...
timeout /t 10 /nobreak >nul

:: ── Start Frontend in new window ─────────────────────────────────────────────
echo  Starting Frontend (React)...
start "WellnessMitra Frontend" cmd /k "set PATH=C:\Program Files\nodejs;%%PATH%% && cd /d "%~dp0\frontend" && echo Frontend starting on http://localhost:3000 && npm start"

:: ── Wait for frontend to start ────────────────────────────────────────────────
echo  Waiting for frontend to compile (15 seconds)...
timeout /t 15 /nobreak >nul

:: ── Open browser ─────────────────────────────────────────────────────────────
echo  Opening app in browser...
start http://localhost:3000

echo.
echo  ========================================================
echo   WellnessMitra is running!
echo.
echo   Frontend  : http://localhost:3000
echo   Backend   : http://localhost:8000
echo   API Docs  : http://localhost:8000/docs
echo.
echo   Close the Backend and Frontend windows to stop the app
echo  ========================================================
echo.
pause
