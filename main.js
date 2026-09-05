const { app, BrowserWindow, dialog, ipcMain } = require("electron");
const path = require("path");
const fs = require("fs");

function createWindow() {
  const win = new BrowserWindow({
    width: 1180,
    height: 800,
    minWidth: 900,
    minHeight: 640,
    title: "图片拼接工具",
    backgroundColor: "#0e1116",
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      preload: path.join(__dirname, "preload.js")
    }
  });

  win.loadFile(path.join(__dirname, "index.html"));

  // 挡掉拖文件进窗口时 Electron 默认"打开文件/导航"的行为，
  // 让渲染进程自己的拖放逻辑能正常接收图片
  win.webContents.setWindowOpenHandler(() => ({ action: "deny" }));
  win.webContents.on("will-navigate", (event, url) => {
    if (url !== win.webContents.getURL()) event.preventDefault();
  });

  // 渲染进程算好拼接图后，把二进制通过 IPC 交主进程：弹“保存”对话框，
  // 既能选目录、又能重命名文件名（默认打开桌面、默认文件名 拼接图-时间戳）
  ipcMain.handle("export-image", async (event, { data, ext }) => {
    const ts = new Date().toISOString().slice(0, 19).replace(/[:T]/g, "-");
    const defaultName = "拼接图-" + ts + "." + ext;
    const result = await dialog.showSaveDialog(win, {
      title: "导出拼接图",
      defaultPath: path.join(app.getPath("desktop"), defaultName),
      filters: ext === "png"
        ? [{ name: "PNG 图片", extensions: ["png"] }]
        : [{ name: "JPEG 图片", extensions: ["jpg", "jpeg"] }]
    });
    if (result.canceled || !result.filePath) {
      return null; // 用户取消
    }
    try {
      fs.writeFileSync(result.filePath, Buffer.from(data));
      dialog.showMessageBox(win, {
        type: "info",
        title: "导出成功",
        message: "拼接图已保存",
        detail: result.filePath
      });
      return result.filePath;
    } catch (err) {
      dialog.showErrorBox("导出失败", (err && err.message) || "写入文件失败");
      throw err;
    }
  });
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
