# 开发说明

## 架构

```
index.html (单文件)
├── <style>        # CSS: 星空、流星、UI 组件样式
├── <canvas>       # Canvas: 星空背景 (starfield)
├── <div> 层       # 流星层、UI 层、照片墙、灯箱
└── <script>       # 全部逻辑
    ├── Starfield      # Canvas 星空渲染
    ├── Meteor System  # 流星生成/动画/回收
    ├── Photo Manager  # 照片加载 (File API + Object URL)
    ├── Photo Wall     # 照片墙 + 灯箱查看
    ├── Music System   # 音乐播放列表 (Audio API)
    └── UI             # 键盘快捷键、Toast、模式切换
```

## 设计原则

1. **零依赖** — 不引入任何 npm 包、CDN、框架
2. **单文件** — 一个 index.html 包含全部内容
3. **双击即用** — Windows 用户双击 setup.bat 或 index.html 直接运行
4. **本地优先** — 照片和音乐通过 File API / Object URL 加载，不上传任何数据

## 星空渲染

- Canvas 自适应窗口
- 星星数量 = `(width * height) / 800`
- 每颗星星独立闪烁周期 (sin 函数)
- 60fps requestAnimationFrame 循环

## 流星系统

- 动态创建 DOM 元素 (div.meteor)
- CSS transition 控制飞行轨迹 (left, top)
- 尾部光晕用 .trail div + linear-gradient 实现
- 生命周期: spawn → fly → fade out → remove
- 间隔时间 = `7000 - speed * 550` ms (speed 1~10)

## 照片管理

- 使用 `URL.createObjectURL()` 创建本地 Object URL
- 支持拖拽 (drop 事件) 和文件选择器
- 内存中维护 photoUrls 数组，不持久化

## 音乐系统

- 基于 HTML5 Audio API
- 播放列表模式，支持上一首/下一首
- Auto-play 受浏览器策略限制，须用户首次交互
- 音量控制和静音切换

## 性能注意事项

- 同时最多约 5-10 个流星 DOM 节点
- 离开页面时自动停止动画 (浏览器节流)
- 照片 Object URL 在页面关闭时自动释放

## 兼容性

- Chrome 90+
- Firefox 90+
- Edge 90+
- Safari 15+
- 不支持 IE
