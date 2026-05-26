# 开发说明

## 架构

```
index.html (单文件, Canvas 渲染引擎)
├── <style>            # UI 层 CSS: 顶栏 / 音乐栏 / 胶片条 / 预览
├── <canvas id="scene"> # 主画布: 星空 + 流星 + 花瓣
├── <div> UI 层         # 上传提示 / 顶栏 / 音乐控制栏 / 胶片条 / 预览浮层
└── <script>           # 全部 JS 逻辑
    ├── Starfield        # Canvas: 200+ 星星 + 15 亮星 + 4 星云团 + 随机流星
    ├── Petals           # Canvas: 40 片玫瑰花瓣，贝塞尔曲线形状
    ├── Meteor System    # Canvas: 椭圆遮罩光球 + 彗尾 + 光晕 + 粒子
    ├── Hit Testing      # 鼠标/触摸碰撞检测
    ├── Filmstrip        # HTML 底部缩略图条 (EXIF 时间排序)
    ├── Preview          # HTML 全屏预览 (图片/GIF/视频)
    ├── Music Player     # HTML5 Audio: 播放列表 / 随机 / 循环 (none/one/all)
    └── Boot             # 启动: 尺寸适配 → 初始化 → 渲染循环
```

## 渲染系统

### 星空 (Canvas)
- 星星数量: 200 普通星 + 15 亮星
- 每颗星独立 sin 闪烁周期
- 亮星 (r>1.5) 附带关联光晕
- 4 个星云团: HSLA 径向渐变
- 背景: 多层径向渐变模拟深空
- 随机流星: 概率 ~0.8%/帧，线性渐变尾迹

### 流星 (Canvas)
- 椭圆裁剪: `ctx.ellipse()` 绘制 oval mask
- 光晕: 外层径向渐变 + 内层径向渐变
- 彗尾: 历史位置轨迹点 (最多 18 个)，径向渐变衰减
- 边缘粒子: 3 个白色粒子绕椭圆边缘旋转
- 悬停: 命中检测 → `scale(1.25)`
- 运动: 正弦/余弦漂移 + 线性速度，屏幕边缘循环

### 花瓣 (Canvas)
- 40 片同时活跃
- 贝塞尔曲线绘制花瓣形状
- HSLA 粉色系着色
- 下落 + 水平摆动 + 旋转
- 超出底部后重置到顶部

### 胶片条 (HTML/CSS)
- 底部固定，默认只露出一小条 (translateY)
- hover 或 pinned 时滑出
- 缩略图按 EXIF 时间排序
- 选中态: 粉色边框 + 上浮 + 光晕
- GIF 标签: 左上角粉色圆点
- 视频标签: 左上角金色圆点

### 预览 (HTML/CSS)
- 全屏浮层，毛玻璃背景
- 图片: `<img>` 显示
- 视频: `<video controls autoplay loop>`
- 键盘: ←→ 切换，Esc 关闭
- 触屏: 点击流星进入，左右按钮导航

## 照片加载

- FileReader API 读取为 Data URL
- Image 对象预加载
- 视频: `URL.createObjectURL()` 生成 blob URL
- EXIF 日期: CDN 加载 exif-js，读取 DateTimeOriginal
- 3 秒超时 → 回退到 `file.lastModified`

## 设计原则

1. Canvas 渲染核心视觉 (星空/流星/花瓣)
2. HTML/CSS 处理 UI 交互 (按钮/胶片条/预览)
3. 双击 index.html 直接运行，无需服务器
4. 单文件自包含 (除外部的 exif-js CDN)

## 键盘快捷键

- **预览打开时**: ←→ 切换，Esc 关闭
- **预览关闭时**: 空格 播放/暂停，←→ 切歌，M 开关音乐栏

## 音乐播放器

- HTML5 Audio API，播放列表 `playlist[]` 存 `{name, url}`
- 循环模式: 0=关闭, 1=单曲循环, 2=列表循环
- 随机播放: `shuffle` 布尔值，切歌时随机选曲
- 自动下一首: `audio.ended` 事件驱动
- UI: 底部可折叠音乐栏，默认隐藏，加载后展开

## music_downloader.py

- 基于 yt-dlp
- `search` / `download` / `batch` / `list` 四个子命令
- 自动转 MP3 320kbps
- 生成 `music/music_manifest.json`

## 导出系统

### 浏览器端导出

顶栏「💝 导出」按钮 → `exportGift()`：

1. 从 `_CLEAN_HTML_SOURCE`（启动时捕获的 `documentElement.outerHTML`）获取页面源码
2. `JSON.stringify` 当前 `photos[]` 和 `playlist[]` 数据（已是 dataUrl/base64）
3. 将 `</` 转义为 `<\/` → `safeEmbedData`
4. `lastIndexOf('</body>')` 找到真正的 HTML 闭合标签，在之前注入 `<script id="embed-data">`
5. 生成 Blob → `<a download>` 触发下载

### 离线批量导出

`build_export.py` — 从磁盘文件生成自包含 HTML：

- 扫描 `Saved Pictures/` 和 `music/` 目录
- 用 Pillow 读取 EXIF 日期
- 文件转 base64 data URL
- 最后一位 `</body>` 之前注入 embed-data（`rfind` 避免误匹配 JS 代码中的字符串）
- 输出 `Memory_Meteor_Shower_YYYY-MM-DD.html`

### 导出文件启动

`bootFromEmbed()` IIFE（`DOMContentLoaded` 事件）：

- 读取 `<script id="embed-data">` 的 JSON
- 图片：`new Image()` 预加载 → 推入 `photos[]`
- 视频：base64 → Blob → `URL.createObjectURL()`
- 音乐：dataUrl 直接推入 `playlist[]`
- 调用 `spawnMeteors()` 和 `renderFilmstrip()` 启动渲染

## 图片压缩

导入时自动压缩（`compressImage()`）：

- WebP 格式，质量 0.72，最大宽度 1600px
- GIF 保持原格式不压缩
- 压缩失败回退到原始 Data URL
- 视频不压缩

## 内存管理

- `blobUrls[]` 追踪所有 `URL.createObjectURL()` 创建的 URL
- `cleanup()` 在 `beforeunload` 事件中释放所有 Blob URL 并取消动画帧

## 兼容性

- Chrome 90+ / Firefox 90+ / Edge 90+ / Safari 15+
- 不支持 IE
