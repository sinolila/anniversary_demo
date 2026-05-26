# Memory Meteor Shower

照片化作流星，划过记忆的星空。

## 这是什么

Memory Meteor Shower 是一个**单文件 HTML 相册应用**——你的照片会变成一颗颗流星，在 Canvas 星空背景中缓缓漂移。

## 功能

| 功能 | 说明 |
|------|------|
| Canvas 星空 | 200+ 闪烁星辰 + 星云辉光 + 随机流星 |
| Canvas 流星 | 椭圆遮罩光球 + 彗尾光晕 + 边缘粒子 + 悬停放大 1.25x |
| Canvas 花瓣 | 40 片粉色玫瑰花瓣持续飘落 |
| 胶片时间轴 | 底部缩略图条，按 EXIF 拍摄时间左旧右新，hover 上浮 |
| 全屏预览 | 图片 / GIF / 视频，键盘 ← → 切换，Esc 关闭 |
| 音乐播放 | 导入本地音乐，支持播放/暂停/切歌/随机/循环三种模式 |
| 拖拽上传 | 支持图片和视频文件，自动取 EXIF 日期排序 |

## 快速开始

**Windows：** 双击 `new_start/index.html` 浏览器打开即用。

**Linux / macOS：**
```bash
cd new_start && python3 -m http.server 8081
# 或 ./dev.sh
```

**移动端：** 将文件发送到手机，用浏览器打开。

## 音乐下载器

使用 `music_downloader.py` 从 YouTube 下载高品质音乐（MP3 320kbps），支持浏览器 Cookie 认证自动绕过反爬。

**前置条件：** `pip install yt-dlp`（Windows 用户双击 `setup.bat` 一键配置）

### 命令

```bash
# 按歌手+歌名搜索下载（输入中文即可）
python music_downloader.py yt "周杰伦 晴天"

# 关键词搜索下载第一个结果
python music_downloader.py search "浪漫钢琴 lofi"

# 交互式搜索：列出前 10 个结果，按序号选择下载
python music_downloader.py find "古风 纯音乐"

# 从 URL 直接下载
python music_downloader.py download "https://youtube.com/watch?v=..."

# 批量下载（读取 songs.txt，每行一首）
python music_downloader.py batch songs.txt

# 查看已下载列表
python music_downloader.py list
```

### Cookie 认证

遇到反爬（如 "Sign in to confirm you're not a bot"）时使用：

```bash
# 指定浏览器读取 Cookie
python music_downloader.py yt "..." --cookies chrome
python music_downloader.py find "..." --cookies firefox
```

支持：`chrome` `firefox` `brave` `edge` `chromium` `opera` `vivaldi`

脚本会自动检测可用浏览器 Cookie（`find` 命令除外，搜索时不强制认证）。

下载的音乐保存在 `music/` 目录，配合相册使用。

## 音乐播放

- 点击顶栏 `🎵` 按钮导入本地音乐文件
- 底部音乐栏：播放/暂停、上一首、下一首
- 随机播放 `🔀` / 循环模式 `🔁`（单曲循环 `🔂` / 列表循环 / 关闭）
- 音量滑块调节
- 键盘快捷键（预览关闭时）：空格 播放暂停 / ←→ 切歌 / M 开关音乐栏

## 导出分享

点击顶栏「💝 导出」按钮，将当前所有照片和音乐打包成一个**自包含 HTML 文件**。别人双击就能看到完整的流星雨画面，无需额外导入任何文件。

也可以从磁盘文件批量生成导出：

```bash
python3 build_export.py
```

脚本自动扫描 `Saved Pictures/` 目录中的图片和 `music/` 目录中的音乐，生成带日期的 `Memory_Meteor_Shower_YYYY-MM-DD.html`。

**注意**：导入图片时自动压缩为 WebP（1600px / 72% 质量），控制导出体积。GIF 和视频保持原格式。

## 设计

- Canvas 全渲染：星空背景 / 流星照片 / 花瓣飘落 全部在 Canvas 上
- HTML/CSS UI 层：顶栏按钮 / 音乐控制栏 / 底部胶片条 / 全屏预览
- EXIF 日期读取：CDN 加载 exif-js，3 秒超时回退到文件日期
- 双击 HTML 直接运行，无需服务器

## 兼容性

- Chrome / Edge / Firefox / Safari 桌面和移动端
- 离线可用（EXIF CDN 加载失败自动回退）
