# anniversary_demo

Memory Meteor Shower — 照片化作流星，划过记忆的星空。

## 项目结构

```
├── new_start/
│   ├── index.html           # 流星雨相册主页面 (单文件应用)
│   ├── music_downloader.py  # yt-dlp 音乐下载器 (搜索/下载/批量)
│   ├── dev.sh               # Linux/macOS 启动脚本
│   ├── setup.bat            # Windows 一键启动 (含 yt-dlp 安装)
│   ├── songs.txt            # 歌单配置
│   ├── music/               # 音乐文件
│   ├── Saved Pictures/      # 照片目录
│   ├── README.md            # 项目介绍 + 操作指南
│   ├── DEV.md               # 开发架构 + 设计原则
│   └── CHANGELOG.md         # 变更记录
├── .gitignore
└── README.md                # 本文档
```

## 快速开始

### Windows
双击 `new_start/setup.bat` — 自动安装 yt-dlp、打开相册。

### Linux / macOS
```bash
cd new_start && bash dev.sh
```

### 手动
浏览器打开 `new_start/index.html`，拖拽照片即可。

## 音乐下载

```bash
pip install yt-dlp
python new_start/music_downloader.py search "浪漫钢琴"
python new_start/music_downloader.py download "YouTube URL"
python new_start/music_downloader.py batch new_start/songs.txt
python new_start/music_downloader.py list
```

## 文档索引

| 文档 | 说明 |
|------|------|
| [new_start/README.md](new_start/README.md) | 项目介绍、功能、操作 |
| [new_start/DEV.md](new_start/DEV.md) | 架构、渲染逻辑、开发习惯 |
| [new_start/CHANGELOG.md](new_start/CHANGELOG.md) | 每次改动的功能变化 |
