# 图片拼接工具

一个轻量、本地运行的图片拼接桌面应用。支持横向 / 竖向 / 四宫格 / 九宫格拼接多张图片，可调节间距、背景色与填充方式，并导出为 PNG / JPG。

> 本工具完全在本地运行，不会上传任何图片，保护隐私。

## ✨ 功能特性

- 🧩 **多种布局**：横向、竖向、四宫格（2 列）、九宫格（3 列）。图片多于格子数会自动加行，不足则末行留空
- 🖱️ **拖拽导入**：拖入多张图片，支持拖拽排序、单张删除
- 📐 **间距调节**：图片之间可设置间距（默认 0px）
- 🎨 **背景设置**：自定义背景色，或透明背景
- 🔍 **填充方式**：网格布局下可选「填满格子（裁切多余）」或「完整显示（留白）」
- 👁️ **实时预览**：参数调整即时反映到预览画面
- 💾 **本地导出**：弹出系统保存对话框，可改名、可选择目录，默认打开「下载」文件夹；支持 PNG / JPG
- 🛡️ **大图保护**：拼接结果超出画布上限时自动等比缩小，并在界面标注
- 🔒 **隐私优先**：纯本地处理，图片不出本机

## 🖥️ 技术栈

- 前端：单文件 `index.html`（原生 HTML / CSS / JavaScript，Canvas 绘制）
- 桌面封装：**Tauri v2**，调用系统 WebView（macOS 为 WKWebView），不内置浏览器内核
- 安装包体积：约 3 MB

## 📦 构建与运行

环境要求：Node.js 18+、Rust 稳定版（建议 1.70+），macOS 自带 WebView。

```bash
cd tauri-app
npm install
npm run tauri build     # 产物在 src-tauri/target/release/bundle/
```

开发预览：

```bash
npm run tauri dev
```

本地直接用浏览器打开根目录 `index.html` 也能使用大部分功能，此时导出走浏览器下载（可选文件名）。

## 🎨 图标

应用图标使用 Pillow 脚本生成：

- `gen_icon.py`：生成当前使用的图标（彩色拼图风格）
- `gen_icons_variants.py`：生成 5 个候选变体（位于 `build/variants/`）

更换图标：把选中的 PNG 复制为 `tauri-app/src-tauri/icon.png`，再在该目录执行 `npx tauri icon icon.png` 重新生成 `.icns`。

## 📁 目录结构

```
.
├── index.html                 # 前端源码（Tauri 与浏览器共用）
├── gen_icon.py                # 图标生成脚本
├── gen_icons_variants.py      # 图标候选生成脚本
├── build/
│   └── variants/              # 5 个图标候选
└── tauri-app/                 # Tauri v2 工程
    ├── frontend/index.html    # Tauri 前端（与根 index.html 一致）
    └── src-tauri/             # Rust + Tauri 配置
```

## 📥 下载

预编译的 macOS（Apple Silicon）安装包在 **GitHub Releases** 中提供，下载 `.dmg` 后拖入「应用程序」即可使用。

## 📜 许可证

[MIT](LICENSE) © 尹瑞林
