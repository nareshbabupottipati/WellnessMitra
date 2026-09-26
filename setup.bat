@echo off
:: ============================================================
::  WellnessMitra — First-Time Setup Script
::  Run this ONCE before starting the app
::  Double-click this file to set up everything automatically
:: ============================================================

title WellnessMitra — Setup

echo.
echo  ██╗    ██╗███████╗██╗     ██╗     ███╗   ██╗███████╗███████╗███████╗
echo  ██║    ██║██╔════╝██║     ██║     ████╗  ██║██╔════╝██╔════╝██╔════╝
echo  ██║ █╗ ██║█████╗  ██║     ██║     ██╔██╗ ██║█████╗  ███████╗███████╗
echo  ██║███╗██║██╔══╝  ██║     ██║     ██║╚██╗██║██╔══╝  ╚════██║╚════██║
echo  ╚███╔███╔╝███████╗███████╗███████╗██║ ╚████║███████╗███████║███████║
echo   ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝
echo.
echo  WellnessMitra — AI Fitness ^& Wellness Agent
echo  First-Time Setup
echo  ================================================================
echo.

:: ── Step 1: Check Python ─────────────────────────────────────────────────────
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  ERROR: Python not found!
    echo  Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)
python --version
echo  OK - Python found
echo.

:: ── Step 2: Check Node.js ─────────────────────────────────────────────────────
echo [2/6] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  ERROR: Node.js not found!
    echo  Please install Node.js 18+ from https://nodejs.org
    pause
    exit /b 1
)
node --version
echo  OK - Node.js found
echo.

:: ── Step 3: Create .env file ──────────────────────────────────────────────────
echo [3/6] Setting up environment file...
if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo  Created .env from .env.example
    echo.
    echo  ================================================================
    echo   ACTION REQUIRED: Open .env and add your API keys!
    echo  ================================================================
    echo.
    echo  Required keys:
    echo    GOOGLE_API_KEY        = Get from https://aistudio.google.com
    echo    GOOGLE_MAPS_API_KEY   = Get from https://console.cloud.google.com
    echo    EDAMAM_APP_ID         = Get from https://developer.edamam.com
    echo    EDAMAM_APP_KEY        = Get from https://developer.edamam.com
    echo.
    echo  Opening .env file for editing...
    timeout /t 2 /nobreak >nul
    notepad .env
    echo.
    set /p CONTINUE="Press ENTER after saving your API keys to continue..."
) else (
    echo  .env already exists - skipping
)
echo.

:: ── Step 4: Python virtual environment ───────────────────────────────────────
echo [4/6] Creating Python virtual environment...
if not exist "venv" (
    python -m venv venv
    echo  Created virtual environment
) else (
    echo  Virtual environment already exists - skipping
)
echo.

:: ── Step 5: Install Python packages ──────────────────────────────────────────
echo [5/6] Installing Python packages (this may take a few minutes)...
call venv\Scripts\activate.bat
pip install --upgrade pip --quiet
pip install -r backend\requirements.txt --quiet
if %errorlevel% neq 0 (
    echo  ERROR: Failed to install Python packages
    pause
    exit /b 1
)
echo  OK - All Python packages installed
echo.

:: ── Step 6: Install Node packages ────────────────────────────────────────────
echo [6/6] Installing frontend packages (this may take a few minutes)...
cd frontend
call npm install --legacy-peer-deps --silent
if %errorlevel% neq 0 (
    echo  ERROR: Failed to install Node packages
    cd ..
    pause
    exit /b 1
)
cd ..
echo  OK - All Node packages installed
echo.

:: ── Step 7: RAG Ingestion ─────────────────────────────────────────────────────
echo [EXTRA] Running RAG knowledge ingestion...
call venv\Scripts\activate.bat
python -m backend.rag.ingestion
if %errorlevel% neq 0 (
    echo  WARNING: RAG ingestion had issues - check your GOOGLE_API_KEY
    echo  The app will still work but knowledge retrieval may be limited
)
echo.

:: ── Done ──────────────────────────────────────────────────────────────────────
echo  ================================================================
echo   Setup Complete! You can now run: start.bat
echo  ================================================================
echo.
echo  Run the app by double-clicking: start.bat
echo.
pause
