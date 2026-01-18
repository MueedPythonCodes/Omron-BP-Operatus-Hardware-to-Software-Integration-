@echo off
title Omron Sync System Loader
cd /d "%~dp0"

echo.
echo ===========================================
echo    OMRON AUTOMATION SYSTEM IS STARTING
echo ===========================================
echo.

:: 1. Virtual Environment ko activate karna
call venv\Scripts\activate

:: 2. Kisi bhi purani phansi hui Flask service ko khatam karna
:: taskkill /F /IM python.exe /T >nul 2>&1

:: 3. Main Script ko background mein run karna
:: Hum 'pythonw' use kar rahe hain taake peeche koi black box na rahe
start pythonw FINAL_AUTO_RUN.py

echo.
echo [SUCCESS] System is running in background.
echo You can close this window now.
echo ===========================================
pause