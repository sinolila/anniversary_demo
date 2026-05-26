#!/usr/bin/env python3
"""Build a self-contained HTML export with embedded images and music.

Scans Saved Pictures/ and music/ directories, converts all files to base64
data URIs, and injects them into index.html so the output file works
standalone — no external files needed.
"""

import base64
import json
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "Saved Pictures")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
INDEX_HTML = os.path.join(BASE_DIR, "index.html")

MIME_MAP = {
    '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
    '.png': 'image/png', '.gif': 'image/gif',
    '.webp': 'image/webp', '.bmp': 'image/bmp',
    '.svg': 'image/svg+xml',
    '.webm': 'audio/webm', '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav', '.ogg': 'audio/ogg',
    '.m4a': 'audio/mp4', '.flac': 'audio/flac',
    '.aac': 'audio/aac',
}

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
AUDIO_EXTS = {'.mp3', '.wav', '.ogg', '.m4a', '.flac', '.webm', '.aac', '.wma'}


def get_mime(filename):
    return MIME_MAP.get(os.path.splitext(filename)[1].lower(),
                        'application/octet-stream')


def try_exif_date(filepath):
    """Try to read DateTimeOriginal EXIF tag; fall back to file mtime."""
    try:
        from PIL import Image
        img = Image.open(filepath)
        exif = img._getexif()
        if exif:
            for tag_id, value in exif.items():
                from PIL.ExifTags import TAGS
                if TAGS.get(tag_id) == 'DateTimeOriginal':
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception:
        pass
    return datetime.fromtimestamp(os.path.getmtime(filepath))


def file_to_dataurl(filepath):
    mime = get_mime(os.path.basename(filepath))
    with open(filepath, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    return f"data:{mime};base64,{b64}"


def main():
    photos = []
    music = []

    # ── Scan images ──
    if os.path.isdir(IMAGES_DIR):
        for fname in sorted(os.listdir(IMAGES_DIR)):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in IMAGE_EXTS:
                continue
            fpath = os.path.join(IMAGES_DIR, fname)
            print(f"  [img] {fname}  ({os.path.getsize(fpath)/1024:.0f} KB)")
            try:
                data_url = file_to_dataurl(fpath)
                date_taken = try_exif_date(fpath)
                photos.append({
                    'name': fname,
                    'dataUrl': data_url,
                    'videoDataUrl': None,
                    'dateTaken': date_taken.isoformat(),
                    'type': 'image',
                    'isGif': ext == '.gif',
                    'isVideo': False,
                })
            except Exception as e:
                print(f"         SKIP: {e}")

    # ── Scan music ──
    if os.path.isdir(MUSIC_DIR):
        for fname in sorted(os.listdir(MUSIC_DIR)):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in AUDIO_EXTS:
                continue
            fpath = os.path.join(MUSIC_DIR, fname)
            size_kb = os.path.getsize(fpath) / 1024
            print(f"  [mus] {fname}  ({size_kb:.0f} KB)")
            try:
                data_url = file_to_dataurl(fpath)
                music.append({'name': fname, 'dataUrl': data_url})
            except Exception as e:
                print(f"         SKIP: {e}")

    if not photos and not music:
        print("No images or music found!")
        sys.exit(1)

    total_img_kb = sum(len(p['dataUrl']) for p in photos) / 1024
    total_mus_kb = sum(len(m['dataUrl']) for m in music) / 1024
    print(f"\n  Photos: {len(photos)}  ({total_img_kb:.0f} KB base64)")
    print(f"  Music:  {len(music)}  ({total_mus_kb:.0f} KB base64)")

    # ── Read template ──
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        html = f.read()

    # ── Build embed JSON ──
    embed = json.dumps({'photos': photos, 'music': music}, ensure_ascii=False)
    safe_embed = embed.replace('</', '<\\/')

    # ── Inject before </body> ──
    # No need to clean pre-existing embed-data: we always read the
    # pristine index.html template which has none.
    tag = f'<script id="embed-data" type="application/json">{safe_embed}</script>'
    # Only replace the LAST </body> (the real HTML tag), not the ones
    # inside JS string literals (e.g. exportGift's html.replace calls).
    last_body = html.rfind('</body>')
    if last_body != -1:
        html = html[:last_body] + tag + '\n</body>' + html[last_body + len('</body>'):]
    else:
        html += '\n' + tag

    # ── Write output ──
    now = datetime.now()
    ds = now.strftime('%Y-%m-%d')
    out_name = f'Memory_Meteor_Shower_{ds}.html'
    out_path = os.path.join(BASE_DIR, out_name)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"\n  => {out_name}  ({size_mb:.1f} MB)")
    print("  Done! Send this file — it works standalone.")


if __name__ == '__main__':
    main()
