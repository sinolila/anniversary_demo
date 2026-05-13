#!/usr/bin/env python3
"""music_downloader.py — yt-dlp 音乐下载器

从 YouTube 搜索/下载高品质音乐（MP3 320kbps），保存到 music/ 目录。

用法:
  python music_downloader.py search "浪漫钢琴 lofi"     # 搜索下载
  python music_downloader.py download "YouTube链接"      # 从URL下载
  python music_downloader.py batch songs.txt            # 批量下载
  python music_downloader.py list                       # 查看已下载

依赖: pip install yt-dlp
"""

import json
import os
import re
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(SCRIPT_DIR, "music")
MANIFEST_FILE = os.path.join(MUSIC_DIR, "music_manifest.json")


def ensure_dir():
    os.makedirs(MUSIC_DIR, exist_ok=True)


def load_manifest():
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_manifest(manifest):
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def check_yt_dlp():
    """检查 yt-dlp 是否可用"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--version"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    try:
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return None


def sanitize_filename(name):
    """清理文件名中的非法字符"""
    name = re.sub(r'[\\/*?:"<>|]', '', name)
    name = name.strip().rstrip('.')
    return name[:120]


def build_yt_dlp_cmd():
    """构建 yt-dlp 基础命令"""
    if subprocess.run([sys.executable, "-m", "yt_dlp", "--version"],
                      capture_output=True, timeout=5).returncode == 0:
        return [sys.executable, "-m", "yt_dlp"]
    return ["yt-dlp"]


def download_audio(query_or_url, search_mode=False):
    """
    下载单首音乐。
    返回 (title, filename) 或 (None, None)
    """
    ensure_dir()
    ytdlp = build_yt_dlp_cmd()

    output_template = os.path.join(MUSIC_DIR, "%(title).120s.%(ext)s")

    cmd = ytdlp + [
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "320K",
        "--output", output_template,
        "--no-playlist",
        "--embed-metadata",
        "--no-overwrites",
        "--print", "after_move:filepath",
        "--print", "title",
    ]

    if search_mode:
        cmd += ["ytsearch1:" + query_or_url]
    else:
        cmd.append(query_or_url)

    print(f"[*] {'搜索' if search_mode else '下载'}: {query_or_url}")
    print(f"[*] 目标目录: {MUSIC_DIR}")
    print()

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            err = result.stderr.strip()
            if err:
                last_err = err.split('\n')[-1]
                print(f"[✗] 下载失败: {last_err}")
            return None, None

        lines = [l.strip() for l in result.stdout.split('\n') if l.strip()]
        title = lines[-1] if lines else "unknown"
        filepath = None
        for l in lines:
            if l.endswith('.mp3') and os.path.exists(l):
                filepath = l
                break

        if not filepath:
            # Try to find the file
            for f in sorted(os.listdir(MUSIC_DIR), key=lambda x: os.path.getmtime(os.path.join(MUSIC_DIR, x)), reverse=True):
                if f.endswith('.mp3'):
                    filepath = os.path.join(MUSIC_DIR, f)
                    break

        if filepath:
            filename = os.path.basename(filepath)
            print(f"[✓] {title}")
            print(f"[✓] 已保存: music/{filename}")
            return title, filename

        print(f"[✗] 未找到输出文件")
        return None, None

    except subprocess.TimeoutExpired:
        print("[✗] 下载超时 (5分钟)")
        return None, None
    except Exception as e:
        print(f"[✗] 错误: {e}")
        return None, None


def cmd_search(query):
    """搜索并下载第一首匹配的音乐"""
    ensure_dir()
    title, filename = download_audio(query, search_mode=True)
    if title and filename:
        manifest = load_manifest()
        manifest[filename] = {
            "title": title,
            "source": f"search: {query}",
            "downloaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        save_manifest(manifest)


def cmd_download(url):
    """从 URL 下载音乐"""
    ensure_dir()
    title, filename = download_audio(url, search_mode=False)
    if title and filename:
        manifest = load_manifest()
        manifest[filename] = {
            "title": title,
            "source": url,
            "downloaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        save_manifest(manifest)


def cmd_batch(songs_file):
    """批量下载 songs.txt 中的音乐"""
    if not os.path.exists(songs_file):
        print(f"[!] 文件不存在: {songs_file}")
        return

    with open(songs_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    print(f"[*] 批量下载 {len(lines)} 首...")
    print()

    for i, line in enumerate(lines, 1):
        print(f"[{i}/{len(lines)}] {line}")
        title, filename = download_audio(line, search_mode=True)
        if title and filename:
            manifest = load_manifest()
            manifest[filename] = {
                "title": title,
                "source": f"batch: {line}",
                "downloaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            save_manifest(manifest)
        if i < len(lines):
            time.sleep(1)  # Rate limit
        print()

    print(f"[*] 批量下载完成")


def cmd_list():
    """列出已下载的音乐"""
    ensure_dir()
    manifest = load_manifest()
    files = sorted(
        [f for f in os.listdir(MUSIC_DIR) if f.endswith('.mp3') and f != "music_manifest.json"],
        key=lambda x: os.path.getmtime(os.path.join(MUSIC_DIR, x)),
        reverse=True
    )

    print("=" * 50)
    print("  music/ 已下载音乐")
    print("=" * 50)
    print()

    if not files:
        print("  (空)")
        print()
        print("[*] 下载音乐:")
        print('  python music_downloader.py search "关键词"')
        return

    for i, f in enumerate(files, 1):
        fpath = os.path.join(MUSIC_DIR, f)
        size_kb = os.path.getsize(fpath) // 1024
        info = manifest.get(f, {})
        title = info.get("title", f.rsplit('.', 1)[0])
        downloaded = info.get("downloaded_at", "")
        print(f"  {i:02d}. {title}")
        print(f"      {f}  |  {size_kb} KB  |  {downloaded}")
        print()

    print(f"  共 {len(files)} 首")


def print_usage():
    print("用法:")
    print('  python music_downloader.py search "浪漫钢琴 lofi"')
    print('  python music_downloader.py download "https://youtube.com/watch?v=..."')
    print("  python music_downloader.py batch songs.txt")
    print("  python music_downloader.py list")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()

    if command == "search":
        if len(sys.argv) < 3:
            print("[!] 请提供搜索关键词")
            print('  例: python music_downloader.py search "浪漫钢琴 lofi"')
            return
        version = check_yt_dlp()
        if not version:
            print("[!] 未安装 yt-dlp，请先执行: pip install yt-dlp")
            return
        print(f"[*] yt-dlp {version}")
        cmd_search(sys.argv[2])

    elif command == "download":
        if len(sys.argv) < 3:
            print("[!] 请提供 YouTube URL")
            print('  例: python music_downloader.py download "https://youtube.com/watch?v=..."')
            return
        version = check_yt_dlp()
        if not version:
            print("[!] 未安装 yt-dlp，请先执行: pip install yt-dlp")
            return
        print(f"[*] yt-dlp {version}")
        cmd_download(sys.argv[2])

    elif command == "batch":
        songs_file = sys.argv[2] if len(sys.argv) > 2 else "songs.txt"
        version = check_yt_dlp()
        if not version:
            print("[!] 未安装 yt-dlp，请先执行: pip install yt-dlp")
            return
        print(f"[*] yt-dlp {version}")
        cmd_batch(songs_file)

    elif command == "list":
        cmd_list()

    else:
        print(f"[!] 未知命令: {command}")
        print_usage()


if __name__ == "__main__":
    main()
