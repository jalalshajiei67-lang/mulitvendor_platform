@echo off
REM CapRover Fresh Installation Script for Windows
REM This script guides you through removing and reinstalling CapRover

setlocal enabledelayedexpansion

echo ========================================
echo   CapRover Fresh Installation Guide
echo ========================================
echo.

:MENU
echo.
echo Select an option:
echo   1. Remove CapRover from server
echo   2. Install fresh CapRover
echo   3. Verify CapRover installation
echo   4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto REMOVE
if "%choice%"=="2" goto INSTALL
if "%choice%"=="3" goto VERIFY
if "%choice%"=="4" goto END
goto MENU

:REMOVE
echo.
echo ========================================
echo   Removing CapRover from Server
echo ========================================
echo.
echo This will remove CapRover and all associated data.
echo.
set /p confirm="Are you sure? (yes/no): "
if /i not "%confirm%"=="yes" goto MENU

echo.
echo Step 1: Uploading removal script...
scp remove-caprover.sh root@158.255.74.123:/root/remove-caprover.sh

if %ERRORLEVEL% NEQ 0 (
    echo Error uploading script. Please check SSH connection.
    pause
    goto MENU
)

echo Step 2: Running removal script...
ssh root@158.255.74.123 "chmod +x /root/remove-caprover.sh && bash /root/remove-caprover.sh"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo CapRover removed successfully!
    echo.
) else (
    echo.
    echo Error removing CapRover. Please check the output above.
    echo.
)
pause
goto MENU

:INSTALL
echo.
echo ========================================
echo   Installing Fresh CapRover
echo ========================================
echo.

echo Step 1: Uploading installation script...
scp install-caprover.sh root@158.255.74.123:/root/install-caprover.sh

if %ERRORLEVEL% NEQ 0 (
    echo Error uploading script. Please check SSH connection.
    pause
    goto MENU
)

echo Step 2: Running installation script...
ssh root@158.255.74.123 "chmod +x /root/install-caprover.sh && bash /root/install-caprover.sh"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo CapRover installed successfully!
    echo.
    echo Next steps:
    echo 1. Open browser: http://158.255.74.123:3000
    echo 2. Complete initial setup:
    echo    - Root domain: indexo.ir
    echo    - Set CapRover password
    echo 3. Login via CLI: caprover login
    echo.
) else (
    echo.
    echo Error installing CapRover. Please check the output above.
    echo.
)
pause
goto MENU

:VERIFY
echo.
echo ========================================
echo   Verifying CapRover Installation
echo ========================================
echo.

echo Checking if CapRover container is running...
ssh root@158.255.74.123 "docker ps | grep captain"

echo.
echo Checking if dashboard is accessible...
curl -s http://158.255.74.123:3000 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Dashboard is accessible at http://158.255.74.123:3000
) else (
    echo Dashboard is not accessible yet. Wait a few minutes and try again.
)

echo.
pause
goto MENU

:END
echo.
echo Exiting...
exit /b 0

