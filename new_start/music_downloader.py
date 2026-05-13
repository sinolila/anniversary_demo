#!/usr/bin/env python3
"""music_downloader.py — 从 songs.txt 读取歌单，模拟下载流程。

因版权原因，不提供真实下载链接。此脚本展示从歌单配置读取，
用户需自行准备音乐文件放入 music/ 目录。
支持 mp3, wav, ogg, flac, m4a 格式。
"""

import os
import sys

MUSIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "music")
SONGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "songs.txt")

SUPPORTED_EXT = {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".wma"}


def read_songs():
    """读取 songs.txt 中的歌曲列表"""
    if not os.path.exists(SONGS_FILE):
        print(f"[!] 歌单文件不存在: {SONGS_FILE}")
        return []
    with open(SONGS_FILE, "r", encoding="utf-8") as f:
        songs = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return songs


def check_existing():
    """检查 music/ 目录已有音乐文件"""
    if not os.path.isdir(MUSIC_DIR):
        return []
    existing = []
    for f in os.listdir(MUSIC_DIR):
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXT:
            existing.append(f)
    return sorted(existing)


def main():
    os.makedirs(MUSIC_DIR, exist_ok=True)

    songs = read_songs()
    existing = check_existing()

    print("=" * 50)
    print("  Memory Meteor Shower — 音乐管理")
    print("=" * 50)
    print()

    if songs:
        print(f"[*] 歌单 ({len(songs)} 首):")
        for i, s in enumerate(songs, 1):
            artist, title = s.split(" - ", 1) if " - " in s else ("", s)
            print(f"    {i:02d}. {title} — {artist}" if artist else f"    {i:02d}. {s}")
        print()

    if existing:
        print(f"[*] music/ 已有 ({len(existing)} 首):")
        for f in existing:
            print(f"    ✓ {f}")
        print()
    else:
        print("[!] music/ 目录为空，请将音乐文件放入 music/ 文件夹")
        print(f"    支持的格式: {', '.join(SUPPORTED_EXT)}")
        print()

    print("[*] 使用说明:")
    print("    1. 编辑 songs.txt 管理歌单")
    print("    2. 将对应音乐文件放入 music/ 目录")
    print("    3. 打开 index.html，点击「加载音乐」选择文件")
    print("    4. 或在 Windows 下双击 setup.bat 启动")
    print()


if __name__ == "__main__":
    main()
