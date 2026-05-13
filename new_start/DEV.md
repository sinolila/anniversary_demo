# 开发说明

## 架构

```
index.html (单文件)
├── <style>           # 星空/流星/花瓣/胶片条/预览 全部 CSS
├── <canvas>          # Canvas: 星空背景 + 星云辉光 + 随机流星
├── <div> 层           # 花瓣层 / 流星层 / UI层 / 胶片条 / 预览
└── <script>          # 全部 JS 逻辑
    ├── Data             # photos[], playlist[], photoMusicMap
    ├── Starfield        # Canvas: 200+ 星星 + 星云 + 随机流星
    ├── Petals           # 40 片玫瑰花瓣 CSS 飘落
    ├── Meteor System    # DOM 流星: 圆形遮罩 + 光晕环 + 彗尾 + 粒子
    ├── Filmstrip        # 底部横向胶片条 (EXIF 时间排序)
    ├── Preview          # 全屏预览 (图片/GIF/视频)
    ├── Music System     # 全局 BGM + 每图专属音乐绑定
    └── UI               # Toast / 键盘快捷键 / 模式切换
```

## 星空系统 (Canvas)

- 星星数量 = `(width * height) / 600`
- 每颗独立 sin 闪烁周期
- 较大星星附带光晕 (径向渐变)
- 星云辉光: 固定位置径向渐变
- 随机流星: 概率生成，线性渐变尾迹，生命周期衰减

## 流星系统 (DOM)

- 圆形遮罩: `border-radius: 50%`
- 光晕环: 脉冲动画 (`pulse-ring`)
- 彗尾: 左侧渐变 div
- 环绕粒子: 6 个白色小点分布在圆形边缘
- 悬停: `scale(1.35)` + 亮度增强 + 光晕放大
- 生命周期: spawn → fly → fade → remove

## 玫瑰花瓣

- 纯 CSS 动画 (`petal-fall`)
- 40 片同时活跃，间隔 0.9s 补充
- 粉色系随机颜色，不规则椭圆形状
- 随机大小/速度/旋转

## 胶片时间轴

- CSS Flexbox 水平排列
- 按 EXIF 拍摄时间 (fallback: 文件修改时间) 左旧右新
- `overflow-x: auto` 水平滚动
- `.music-badge` 金色音符标记绑定音乐的照片

## 预览系统

- 图片: `<img>` 显示
- GIF: 自动播放
- 视频: `<video controls autoplay>`
- 键盘 ← → 切换，Esc 关闭
- 右下 🎵 按钮绑定/取消专属音乐

## 音乐系统

- 全局 BGM: 播放列表循环
- 每图专属: `photoMusicMap` (URL → playlistIndex)
- 预览时自动切换到专属音乐，关闭后回到全局 BGM
- 曲目名称顶部显示 (4s 自动淡出)
- Audio API 浏览器自动播放策略: 须用户首次交互

## 设计原则

1. **零依赖** — 不引入 npm / CDN / 框架
2. **单文件** — index.html 自包含一切
3. **双击即用** — Windows 双击 index.html 或 setup.bat
4. **本地优先** — File API + Object URL，零网络请求

## music_downloader.py

- 基于 yt-dlp
- `search` / `download` / `batch` / `list` 四个子命令
- 自动转 MP3 320kbps
- 生成 `music/music_manifest.json`

## 兼容性

- Chrome 90+ / Firefox 90+ / Edge 90+ / Safari 15+
- 不支持 IE
