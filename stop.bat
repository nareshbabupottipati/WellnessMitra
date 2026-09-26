@echo off
:: ============================================================
::  WellnessMitra — Stop Application
::  Kills all running backend and frontend processes
:: ============================================================
echo  Stopping WellnessMitra...
taskkill /f /im uvicorn.exe    >nul 2>&1
taskkill /f /im python.exe     >nul 2>&1
taskkill /f /im node.exe       >nul 2>&1
echo  All services stopped.
timeout /t 2 /nobreak >nul
