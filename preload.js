const { contextBridge, ipcRenderer } = require("electron");

// 只暴露最小、明确的能力给渲染进程
contextBridge.exposeInMainWorld("stitchApi", {
  exportImage: (data, ext) =>
    ipcRenderer.invoke("export-image", { data, ext })
});
