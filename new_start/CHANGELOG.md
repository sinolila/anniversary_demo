# 变更记录

---

## [2026-05-14] 项目重建

### 新增
- **index.html**: 完整的流星雨相册应用
  - Canvas 星空背景 (60fps 自适应)
  - 流星模式: 照片以流星形式飘过屏幕
  - 照片墙模式: 网格浏览所有照片
  - 灯箱查看: 点击放大
  - 音乐播放系统: 播放列表、上下曲、音量控制
  - 拖拽加载照片、文件选择器加载音乐
  - 键盘快捷键 (空格/←→/M/Esc/F)
  - 流星速度调节滑块
- **music_downloader.py**: 音乐管理脚本
- **dev.sh**: Linux/macOS 启动脚本
- **setup.bat**: Windows 一键启动
- **songs.txt**: 歌单配置文件
- **README.md**: 项目介绍文档
- **DEV.md**: 开发说明文档
- **CHANGELOG.md**: 本文档 (变更记录)

### 技术栈
- 纯 HTML5 + CSS3 + JavaScript
- Canvas 星空渲染
- CSS Transition 流星动画
- File API + Object URL 本地文件加载
- Audio API 音乐播放

---

> 格式参考: [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
