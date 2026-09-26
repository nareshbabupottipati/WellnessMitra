@echo off
:: ============================================================
::  WellnessMitra — Backend Only (for testing/debugging)
:: ============================================================
title WellnessMitra Backend
cd /d "%~dp0"
call venv\Scripts\activate.bat
echo.
echo  Backend starting on http://localhost:8000
echo  API Docs:  http://localhost:8000/docs
echo  Press Ctrl+C to stop
echo.
uvicorn backend.api.main:app --reload --port 8000 --host 0.0.0.0
