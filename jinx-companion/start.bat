@echo off
setlocal

:: Jinx Companion - Windows Startup Script
:: Opens the chat app in your default browser

echo Starting Jinx Companion server...

timeout /t 1 >nul

:: Start the Python server in the background
start "Jinx Companion Server" python "%~dp0server.py"

:: Wait a moment for the server to start
timeout /t 2 >nul

:: Open the browser
start "" "http://127.0.0.1:8720"

echo Server should be running at http://127.0.0.1:8720
pause
