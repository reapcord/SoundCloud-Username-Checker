@echo off
title @demiourgia
color 0a
echo.
echo [*] Setting up SC Username Checker...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH
    echo [*] Downloading Python installer...
    powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe', 'python-installer.exe')"
    echo [*] Installing Python...
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
    echo [*] Python installed successfully
) else (
    echo [*] Python is already installed
)

echo.
echo [*] Installing required packages...
pip install requests colorama

echo.
echo [*] Creating configuration files...
(
echo {
echo     "webhook": "",
echo     "webhook_name": "SC Checker", 
echo     "webhook_pfp": "",
echo     "theme": "Demiourgia"
echo }
) > config.json

echo. > wordlist.txt
echo. > available.txt

echo.
echo [*] @unburdening
echo [*] python demiourgia.py
echo.
pause