@echo off
chcp 65001 >nul
title Memory Meteor Shower - Setup

echo ================================
echo   Memory Meteor Shower
echo ================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] 未找到 Python，请先安装 Python 3
    echo     下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [*] Python 已就绪
echo.

:: Run music management
cd /d "%~dp0"
python music_downloader.py
echo.

:: Open browser
echo [*] 正在打开浏览器...
start "" "%~dp0index.html"

echo.
echo [*] 提示: 将音乐文件放入 music 文件夹后点击「加载音乐」
echo [*] 按 F 加载照片，按 空格 播放/暂停音乐
pause
