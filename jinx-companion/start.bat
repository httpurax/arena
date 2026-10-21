@echo off
setlocal

:: Jinx Companion - Windows Startup Script
:: Starts the local server. The server itself opens the chat app in the
:: browser (exactly one tab), so this script must not open one too.

echo Starting Jinx Companion server...

timeout /t 1 >nul

:: Start the Python server in the background
start "Jinx Companion Server" python "%~dp0server.py"

echo Server should be running at http://127.0.0.1:8720
pause
