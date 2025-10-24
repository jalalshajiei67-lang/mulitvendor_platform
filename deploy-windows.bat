@echo off
REM Windows Deployment Script for Multivendor Platform

echo ========================================
echo Multivendor Platform - Windows Deploy
echo ========================================
echo.

REM Configuration
set VPS_IP=158.255.74.123
set VPS_USER=root
set PROJECT_NAME=multivendor_platform
set REMOTE_DIR=/opt/%PROJECT_NAME%

REM Check if .env exists
if not exist ".env" (
    echo Error: .env file not found!
    echo Please create .env file from env.template
    echo.
    echo   copy env.template .env
    echo   REM Then edit .env with your configuration
    pause
    exit /b 1
)

echo Step 1: Creating deployment package...
echo.

REM Create deployment archive using tar (Windows 10+)
tar -czf deploy.tar.gz ^
    --exclude=node_modules ^
    --exclude=venv ^
    --exclude=*.pyc ^
    --exclude=__pycache__ ^
    --exclude=.git ^
    --exclude=*.sqlite3 ^
    --exclude=.env ^
    --exclude=multivendor_platform\multivendor_platform\media ^
    --exclude=multivendor_platform\front_end\dist ^
    docker-compose.yml ^
    nginx ^
    Dockerfile ^
    requirements.txt ^
    multivendor_platform

if %ERRORLEVEL% NEQ 0 (
    echo Error creating deployment package
    pause
    exit /b 1
)

echo Success: Deployment package created
echo.

echo Step 2: Uploading to VPS...
echo.

REM Upload files using SCP
scp deploy.tar.gz %VPS_USER%@%VPS_IP%:/tmp/
scp .env %VPS_USER%@%VPS_IP%:/tmp/deploy.env
scp server-deploy.sh %VPS_USER%@%VPS_IP%:/tmp/
scp setup-ssl.sh %VPS_USER%@%VPS_IP%:/tmp/
scp manage-deployment.sh %VPS_USER%@%VPS_IP%:/tmp/

if %ERRORLEVEL% NEQ 0 (
    echo Error uploading files
    pause
    exit /b 1
)

echo Success: Files uploaded
echo.

echo Step 3: Setting up on VPS...
echo.

REM Execute setup commands on VPS
ssh %VPS_USER%@%VPS_IP% "mkdir -p %REMOTE_DIR% && cd %REMOTE_DIR% && tar -xzf /tmp/deploy.tar.gz && mv /tmp/deploy.env .env && mv /tmp/server-deploy.sh . && mv /tmp/setup-ssl.sh . && mv /tmp/manage-deployment.sh . && chmod +x *.sh && rm /tmp/deploy.tar.gz"

if %ERRORLEVEL% NEQ 0 (
    echo Error setting up on VPS
    pause
    exit /b 1
)

REM Clean up local deployment package
del deploy.tar.gz

echo.
echo ========================================
echo Deployment Package Uploaded!
echo ========================================
echo.
echo Next steps:
echo 1. SSH into your VPS:
echo    ssh %VPS_USER%@%VPS_IP%
echo.
echo 2. Navigate to project directory:
echo    cd %REMOTE_DIR%
echo.
echo 3. Run server deployment:
echo    ./server-deploy.sh
echo.
echo Or use the management interface:
echo    ./manage-deployment.sh
echo.
pause



