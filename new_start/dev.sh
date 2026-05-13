#!/bin/bash
# dev.sh — Memory Meteor Shower 开发/启动脚本
# 用法: bash dev.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "================================"
echo "  Memory Meteor Shower"
echo "================================"
echo ""

# 检查音乐文件
if [ -d "$SCRIPT_DIR/music" ] && [ "$(ls -A "$SCRIPT_DIR/music" 2>/dev/null)" ]; then
    count=$(ls "$SCRIPT_DIR/music" | wc -l)
    echo "[*] music/ 已有 $count 个文件"
else
    echo "[!] music/ 为空，请放入音乐文件或使用「加载音乐」按钮"
fi

# 运行音乐管理脚本
if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/music_downloader.py"
elif command -v python &>/dev/null; then
    python "$SCRIPT_DIR/music_downloader.py"
fi

echo ""
echo "[*] 在浏览器中打开:"
echo "    file://$SCRIPT_DIR/index.html"
echo ""

# 尝试自动打开浏览器
if command -v xdg-open &>/dev/null; then
    xdg-open "$SCRIPT_DIR/index.html" 2>/dev/null &
elif command -v open &>/dev/null; then
    open "$SCRIPT_DIR/index.html" 2>/dev/null &
elif command -v start &>/dev/null; then
    start "$SCRIPT_DIR/index.html" 2>/dev/null &
else
    echo "[!] 请手动在浏览器中打开上述地址"
fi
