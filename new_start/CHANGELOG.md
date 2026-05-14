# 变更记录

---

## [2026-05-15] 音乐播放器 + 快捷键

### 新增
- 音乐播放系统：导入本地音频 → 底部控制栏
  - 播放/暂停、上一首/下一首
  - 随机播放 `🔀`、循环模式 `🔁`（单曲循环/列表循环/关闭）
  - 音量滑块
- 键盘快捷键：空格（播放/暂停）、←→（切歌）、M（开关音乐栏）
- music_downloader.py 已使用 yt-dlp，自动选最佳音质转 MP3 320kbps

---

## [2026-05-15] 审计修复

### 修复
- 从 diff 视图还原 index.html 源码，修复 6 个 diff 残留问题
- 补全 `--text`、`--rose` CSS 变量
- 修复 `fmtDate`/`fmtShort` 合并冲突

---

## [2026-05-14] Canvas 渲染版

### 技术栈
- Canvas 全渲染：星空背景（200+ 星 + 星云 + 随机流星）、流星照片（椭圆遮罩 + 彗尾 + 粒子）、玫瑰花瓣（40 片贝塞尔曲线）
- HTML/CSS UI 层：顶栏按钮、底部胶片时间轴、全屏预览浮层
- EXIF 日期读取（CDN + 3s 超时回退）
- 拖拽上传照片/视频，自动排序

### 辅助脚本
- `music_downloader.py`: 基于 yt-dlp 的音乐下载器（search/download/batch/list）
- `dev.sh` / `setup.bat` / `songs.txt`

---

> 格式参考: [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
