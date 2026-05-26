# CLAUDE.md — Memory Meteor Shower

## 项目概要
单文件 Canvas 相册应用 (`new_start/index.html`)，照片化作流星在星空中漂移。双击即可在 Windows 上运行。

## 核心约束
- **不要引入 npm / build 工具 / 框架** — 保持单文件自包含
- **不要拆分 index.html** — 所有 CSS/JS 在一个文件内
- **双击即用** — 不能在启动流程里加命令行步骤
- **Canvas 渲染核心视觉** — 星空/流星/花瓣走 Canvas，UI 控

件走 HTML/CSS

## 关键文件
- `new_start/index.html` — 主程序 (Canvas 引擎 + UI + 自导出)
- `new_start/music_downloader.py` — yt-dlp 下载器
- `new_start/build_export.py` — 从磁盘文件批量生成自包含导出 HTML
- `new_start/setup.bat` — Windows 一键启动

## 文档
- `new_start/README.md` — 功能说明 + 操作指南
- `new_start/DEV.md` — 架构详解
- `new_start/CHANGELOG.md` — 变更记录
