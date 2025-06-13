const { contextBridge, ipcRenderer, webUtils } = require('electron')


contextBridge.exposeInMainWorld('electron', {
    node: () => process.versions.node,
    chrome: () => process.versions.chrome,
    electron: () => process.versions.electron,
});

contextBridge.exposeInMainWorld('main', {
    onMenuActions: (callback) => ipcRenderer.on('menu-actions', (_event, action) => callback(action)),
});

contextBridge.exposeInMainWorld('fs', {
    getLspConfigData: () => ipcRenderer.invoke("getLspConfigData"),
    getFileContents: (path) => ipcRenderer.invoke("getFileContents", path),
    openFiles: (startPath) => ipcRenderer.invoke("openFiles", startPath),
    saveFile: (path, content) => ipcRenderer.invoke("saveFile", path, content),
    saveFileAs: (content) => ipcRenderer.invoke("saveFileAs", content),
    closeFile: (path) => ipcRenderer.invoke("closeFile", path),
    getPathForFile: (file) => webUtils.getPathForFile(file),
    onLoadFiles: (callback) => ipcRenderer.on('load-files', (_event, paths) => callback(paths)),
});