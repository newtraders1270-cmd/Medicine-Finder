@echo off
title MediCompare - Medicine Locator & Price Comparison Web Application
color 0A

echo ======================================================================
echo              Medicine Availability Finder Web Portal
echo               T.Y.C.S. Mini Project - Kaustubh Mhatre
echo ======================================================================
echo.

echo [1/3] Checking Python installation...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found! Please ensure Python is installed.
    pause
    exit /b
)
py --version

echo.
echo [2/3] Checking dependencies...
py -m pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Could not auto-install requirements. Attempting to continue...
)

echo.
echo [3/3] Checking database file...
if not exist medicompare.db (
    echo Database not found. Initializing and seeding demo data...
    py seed_data.py
) else (
    echo Database file found: medicompare.db
)

echo.
echo ======================================================================
echo  Server is starting! 
echo  Open your web browser and navigate to:
echo  --^> http://127.0.0.1:5000
echo ======================================================================
echo.
echo Demo Logins:
echo   - Customer:  customer@demo.com  (Password: password123)
echo   - Store:     apollo@demo.com    (Password: password123)
echo   - Supplier:  metro@demo.com     (Password: password123)
echo   - Admin:     admin@demo.com     (Password: password123)
echo.
echo Press Ctrl+C in this terminal window to stop the server anytime.
echo.

py app.py
pause

