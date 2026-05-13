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

:: Install yt-dlp (music downloader)
echo [*] 配置音乐下载环境...
pip install yt-dlp --quiet
if %errorlevel% equ 0 (
    echo [*] yt-dlp 已就绪
) else (
    echo [!] yt-dlp 安装失败，音乐下载功能不可用
)
echo.

:: Run music management
cd /d "%~dp0"
python music_downloader.py list
echo.

:: Open browser
echo [*] 正在打开浏览器...
start "" "%~dp0index.html"

echo.
echo [*] 提示:
echo     - 拖拽照片到窗口即可加载
echo     - 点击「🎵 音乐」加载背景音乐
echo     - 预览照片时点击右下 🎵 绑定专属音乐
echo     - 下载音乐: python music_downloader.py search "关键词"
echo.
pause
