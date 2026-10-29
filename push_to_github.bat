@echo off
title Push to GitHub - Medicine Availability Finder
color 0B

echo ======================================================================
echo           Medicine Availability Finder - Push to GitHub
echo               T.Y.C.S. Mini Project - Kaustubh Mhatre
echo ======================================================================
echo.
echo Step 1: Create a NEW repository on GitHub:
echo         Open your browser: https://github.com/new
echo         Repository name: medicine-availability-finder
echo         Visibility: Public
echo         (Do NOT check "Add a README" or ".gitignore")
echo         Click "Create repository"
echo.
echo Step 2: Paste your GitHub repository URL below.
echo         Example: https://github.com/kaustubh-mhatre/medicine-availability-finder.git
echo.
set /p REPO_URL="Enter your GitHub Repo URL: "

if "%REPO_URL%"=="" (
    echo [ERROR] No URL entered. Exiting...
    pause
    exit /b
)

echo.
echo Connecting to GitHub repository...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git branch -M main

echo Pushing code to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ======================================================================
    echo  SUCCESS! Code pushed to GitHub!
    echo.
    echo  NOW TO GET YOUR LIVE LINK (GitHub Pages):
    echo  1. Open your repo on GitHub in browser
    echo  2. Click "Settings" (top right of repo)
    echo  3. Click "Pages" (left sidebar)
    echo  4. Under "Branch", select "main" and folder "/docs"
    echo  5. Click "Save"
    echo.
    echo  Your Live Website Link will be:
    echo  --^> https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/
    echo ======================================================================
) else (
    echo.
    echo [ERROR] Git push failed. Please check your GitHub credentials or URL.
)

pause

