# 图片拼接工具

一个轻量、本地运行的图片拼接桌面应用。支持横向 / 竖向拼接多张图片，可调节间距、背景色、等比缩放，并导出为 PNG / JPG。

> 本工具完全在本地运行，不会上传任何图片，保护隐私。

## ✨ 功能特性

- 🧩 **多图拼接**：支持横向、竖向两种拼接方向
- 🖱️ **拖拽导入**：拖入多张图片，支持拖拽排序、单张删除
- 📐 **间距调节**：图片之间可设置间距（默认 0px）
- 🎨 **背景设置**：自定义背景色，或透明背景
- 🔍 **等比缩放**：可选对图片做等比缩放后再拼接
- 👁️ **实时预览**：参数调整即时反映到预览画面
- 💾 **本地导出**：导出时弹出系统保存对话框，可重命名、默认保存到桌面；支持 PNG / JPG
- 🔒 **隐私优先**：纯本地处理，图片不出本机

## 🖥️ 技术栈

同一套前端 UI，提供两种桌面打包方式：

| 方案 | 体积 | 说明 |
|------|------|------|
| **Tauri（推荐）** | ~3.2 MB | 基于系统 WebView，体积小、资源占用低，适合分发 |
| Electron | ~105 MB | 内置 Chromium，兼容性强 |

## 📦 构建与运行

### 方式一：Tauri（推荐）

环境要求：Node.js 18+，Rust 稳定版（建议 1.70+），macOS 自带 WebView。

```bash
cd tauri-app
npm install
npm run tauri build     # 产物在 src-tauri/target/release/bundle/
```

开发预览：

```bash
npm run tauri dev
```

### 方式二：Electron

环境要求：Node.js 18+。

```bash
npm install
npm start               # 启动应用
npm run dist            # 打包 dmg（输出到 dist/）
```

## 🎨 图标

应用图标使用 Pillow 脚本生成：

- `gen_icon.py`：生成当前使用的图标（彩色拼图风格）
- `gen_icons_variants.py`：生成 5 个候选变体（位于 `build/variants/`）

更换图标后，进入 `tauri-app/src-tauri` 执行 `npx tauri icon icon.png` 重新生成 `.icns`。

## 📁 目录结构

```
.
├── index.html                 # 独立 Web 版 / Electron 前端
├── main.js / preload.js       # Electron 主进程
├── package.json               # Electron 构建配置
├── gen_icon.py                # 图标生成脚本
├── gen_icons_variants.py      # 图标候选生成脚本
├── build/
│   ├── icon_1024.png          # 图标源图
│   └── variants/              # 5 个图标候选
└── tauri-app/                 # Tauri v2 工程
    ├── frontend/index.html    # Tauri 前端（与根 index.html 一致）
    └── src-tauri/             # Rust + Tauri 配置
```

## 📥 下载

预编译的 macOS（Apple Silicon）安装包在 **GitHub Releases** 中提供，下载 `.dmg` 后拖入「应用程序」即可使用。

## 📜 许可证

[MIT](LICENSE) © 尹瑞林
