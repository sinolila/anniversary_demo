# 开发说明

## 架构

```
index.html (单文件, Canvas 渲染引擎)
├── <style>            # UI 层 CSS: 顶栏 / 胶片条 / 预览
├── <canvas id="scene"> # 主画布: 星空 + 流星 + 花瓣
├── <div> UI 层         # 上传提示 / 顶栏 / 胶片条 / 预览浮层
└── <script>           # 全部 JS 逻辑
    ├── Starfield        # Canvas: 200+ 星星 + 15 亮星 + 4 星云团 + 随机流星
    ├── Petals           # Canvas: 40 片玫瑰花瓣，贝塞尔曲线形状
    ├── Meteor System    # Canvas: 椭圆遮罩光球 + 彗尾 + 光晕 + 粒子
    ├── Hit Testing      # 鼠标/触摸碰撞检测
    ├── Filmstrip        # HTML 底部缩略图条 (EXIF 时间排序)
    ├── Preview          # HTML 全屏预览 (图片/GIF/视频)
    └── Boot             # 启动: 尺寸适配 → 星空/花瓣初始化 → 渲染循环
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

## music_downloader.py

- 基于 yt-dlp
- `search` / `download` / `batch` / `list` 四个子命令
- 自动转 MP3 320kbps
- 生成 `music/music_manifest.json`

## 兼容性

- Chrome 90+ / Firefox 90+ / Edge 90+ / Safari 15+
- 不支持 IE
