@echo off
:: ============================================================
::  WellnessMitra — Frontend Only (for UI testing)
:: ============================================================
title WellnessMitra Frontend
cd /d "%~dp0\frontend"
echo.
echo  Frontend starting on http://localhost:3000
echo  Press Ctrl+C to stop
echo.
npm start
