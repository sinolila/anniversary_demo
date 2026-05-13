# Memory Meteor Shower

照片化作流星，划过记忆的星空。

## 这是什么

Memory Meteor Shower 是一个**单文件 HTML 相册应用**——你的照片会变成一颗颗流星，在星空背景中缓缓划过。

- **无需安装**：双击 index.html 即可运行
- **无需依赖**：没有 npm / build / 框架，纯原生 HTML5
- **拖拽即用**：将照片拖入窗口即可加载
- **自带音乐系统**：加载本地音乐，流星 + BGM

## 快速开始

### Windows
双击 `setup.bat`

### Linux / macOS
```bash
bash dev.sh
```

### 手动打开
直接用浏览器打开 `index.html`

## 操作说明

| 操作 | 方式 |
|------|------|
| 加载照片 | 点击「加载照片」或拖拽图片到窗口 |
| 加载音乐 | 点击「加载音乐」选择音频文件 |
| 切换模式 | 流星模式 / 照片墙 |
| 播放控制 | 底部音乐栏 / 空格键 |
| 切歌 | ← → 方向键 |
| 静音 | M 键 |
| 关闭灯箱 | Esc 键 |
| 调整流速 | 顶部滑块 |

## 文件结构

```
new_start/
├── index.html           # 主程序 (单文件)
├── music_downloader.py  # 音乐管理脚本
├── dev.sh               # Linux/macOS 启动脚本
├── setup.bat            # Windows 一键启动
├── songs.txt            # 歌单配置
├── music/               # 音乐文件目录
├── Saved Pictures/      # 照片目录
├── README.md            # 本文档 (项目介绍)
├── DEV.md               # 开发说明
└── CHANGELOG.md         # 变更记录
```

## 技术栈

纯 HTML5 + CSS3 + JavaScript，使用 Canvas 渲染星空背景，CSS Transition 驱动流星动画，Web Audio 播放音乐。
