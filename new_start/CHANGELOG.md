# 变更记录

---

## [2026-05-27] 导出功能修复 + build_export.py

### 修复 (index.html)
- 修复 `exportGift()` 正则误删 JS 代码：`/<script\s+id="embed-data"[^>]*>[\s\S]*?<\/script>/gi` 匹配到了 `exportGift` 自身代码中的字符串字面量，删除正则清理步骤
- 修复 `exportGift()` 注入位置错误：`html.replace('</body>', ...)` 只替换第一个 `</body>`（在 JS 代码字符串内），改为 `lastIndexOf('</body>')` + slice 拼接

### 新增
- `build_export.py` — 从磁盘文件批量生成自包含导出 HTML（扫描 Saved Pictures/ + music/，Pillow 读 EXIF，base64 内嵌）

---

## [2026-05-22] 代码审查修复

### 修复 (index.html)
- 添加 Blob URL 生命周期管理：所有 `URL.createObjectURL()` 创建的 URL 统一追踪，在页面卸载时通过 `URL.revokeObjectURL()` 释放，防止内存泄漏
- 添加 `beforeunload` 清理回调：页面关闭时取消 `requestAnimationFrame` 并释放所有 Blob URL
- 添加拖拽上传支持：支持直接将文件拖拽到页面上传（`dragover`/`dragenter`/`drop` 事件）
- `readBlob()` 和 `loadImg()` 添加 `onerror` 错误处理：损坏/不支持的图片不再导致 Promise 永久挂起
- `handleFiles()` 添加 try-catch：单个文件加载失败不阻塞其余文件，并通过 toast 提示用户
- `handleMusicFiles()` 音乐 Blob URL 纳入统一追踪
- 移除 `spawnMeteors()` 中未使用的 `angle` 和 `dist` 变量
- Canvas resize 事件添加 200ms 防抖（debounce），避免拖拽窗口时的频繁重计算
- 修复 `exportGift()` 语法错误：`};r` → `};`，导致导出功能完全不可用
- 修复导出 HTML 页面显示原始 JavaScript 代码的问题：根因是 base64 编码数据中可能出现 `</script>` 子串，导致 HTML 解析器提前关闭 `<script id="embed-data">` 标签，后续所有内容被当作纯文本渲染。修复方案：写入 JSON 前将 `</` 转义为 `<\/`（JSON 标准合法转义，`JSON.parse` 读取时自动还原）
- 修复导出 `</script>` 闭合标签错误：`<\/script>` 在 HTML 中不会被浏览器识别为闭合标签，导致注入的 `#embed-data` 永不闭合。改为 JS 字符串拼接 `'</' + 'script>'`
- 修复导出 HTML 数据永不被加载的核心 bug：`bootFromEmbed` 是 IIFE，在 `<script>` 块解析时立即执行，此时 HTML 解析器尚未到达 `#embed-data` 标签，`getElementById` 始终返回 `null`。改为 `DOMContentLoaded` 事件，确保在完整 DOM 解析后再恢复数据
- 新增启动时 `_CLEAN_HTML_SOURCE = document.documentElement.outerHTML` 捕获原始 HTML 源，导出时直接使用，彻底绕过 XHR/fetch 在 `file://` 协议下的限制
- `exportGift()` 移除了 30 行的 XHR/fetch/DOM 序列化回退链，替换为单行 `_CLEAN_HTML_SOURCE` 引用
- 新增 `compressImage()` 图片压缩函数：导入图片时自动转为 WebP 格式（质量 72%，宽度限制 1600px），GIF 保持原格式不压缩，大幅减小导出的 HTML 体积
- 升级 `readBlob()`：图片类型文件导入时自动走压缩流程，压缩失败时回退到原始 Data URL
- 升级音乐存储方式：`handleMusicFiles()` 改为将音乐文件读取为 Data URL 而非 Blob URL，确保导出的 HTML 中音乐不依赖本地文件
- playlist 数据结构统一为 `{name, dataUrl}`，所有 `.url` 引用改为 `.dataUrl`
- 重写 `exportGift()`：图片已自动压缩存储、音乐已用 Data URL 存储，导出时直接复用无需二次转换（仅视频仍需 readBlob）
- 重写 `bootFromEmbed()` 音乐段：适配新的 `{name, dataUrl}` 格式
- 修复 `tl = html.replace` 笔误 → `html = html.replace`（导致导出文件被截断）
- 修复导出 dataScript 注入时 `embedData` 未使用 `safeEmbedData`（`</script>` 截断保护丢失）

### 修复 (music_downloader.py)
- 移除 `detect_browser_cookies()` 中未使用的 `import shutil as _shutil`
- 异常捕获从宽泛的 `except Exception` 改为具体的 `except (subprocess.SubprocessError, OSError)`，避免吞没 `KeyboardInterrupt` 等信号
- `build_yt_dlp_cmd()` 添加结果缓存，避免重复执行子进程检查
- `batch` 命令的默认 `songs.txt` 路径改为基于脚本目录 (`SCRIPT_DIR`)，不再依赖当前工作目录

---

## [2026-05-15] 音乐播放器 + 快捷键

### 新增
- 音乐播放系统：导入本地音频 → 底部控制栏
  - 播放/暂停、上一首/下一首
  - 随机播放 `?`、循环模式 `?`（单曲循环/列表循环/关闭）
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
