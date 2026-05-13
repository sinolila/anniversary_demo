# anniversary_demo

Memory Meteor Shower — 照片化作流星，划过记忆的星空。

## 项目结构

```
├── new_start/               # 主项目目录
│   ├── index.html           # 流星雨相册主页面 (单文件应用)
│   ├── music/               # 背景音乐文件
│   ├── Saved Pictures/      # 照片存放目录
│   ├── music_downloader.py  # 音乐管理脚本
│   ├── dev.sh               # Linux/macOS 启动脚本
│   ├── setup.bat            # Windows 一键启动 (双击运行)
│   ├── songs.txt            # 歌单配置
│   ├── README.md            # 项目介绍
│   ├── DEV.md               # 开发说明
│   └── CHANGELOG.md         # 变更记录
├── .gitignore
└── README.md                # 本文档
```

## 快速开始

### Windows
双击 `new_start/setup.bat` 自动启动。

### Linux / macOS
```bash
cd new_start
bash dev.sh
```

### 手动
直接用浏览器打开 `new_start/index.html`，拖拽照片开始体验。

## 文档索引

| 文档 | 说明 |
|------|------|
| [new_start/README.md](new_start/README.md) | 项目介绍、操作指南 |
| [new_start/DEV.md](new_start/DEV.md) | 开发架构、设计原则 |
| [new_start/CHANGELOG.md](new_start/CHANGELOG.md) | 功能/内容变更记录 |
