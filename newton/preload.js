const { contextBridge, ipcRenderer, webUtils } = require('electron')


contextBridge.exposeInMainWorld('electron', {
    node: () => process.versions.node,
    chrome: () => process.versions.chrome,
    electron: () => process.versions.electron,
});

contextBridge.exposeInMainWorld('main', {
    onMenuActions: (callback) => ipcRenderer.on('menu-actions', (_event, action) => callback(action)),
    onTerminalActions: (callback) => ipcRenderer.on('terminal-actions', (_event, action) => callback(action)),
    quit: () => ipcRenderer.invoke("quit"),
    toggleFullScreen: () => ipcRenderer.invoke("toggleFullScreen"),
});

contextBridge.exposeInMainWorld('fs', {
    getLspConfigData: () => ipcRenderer.invoke("getLspConfigData"),
    getFileContents: (path) => ipcRenderer.invoke("getFileContents", path),
    openFiles: (startPath) => ipcRenderer.invoke("openFiles", startPath),
    saveFile: (path, content) => ipcRenderer.invoke("saveFile", path, content),
    saveFileAs: () => ipcRenderer.invoke("saveFileAs"),
    chooseFolder: () => ipcRenderer.invoke("chooseFolder"),
    closeFile: (path) => ipcRenderer.invoke("closeFile", path),
    getPathForFile: (file) => webUtils.getPathForFile(file),
    onLoadFiles: (callback) => ipcRenderer.on('load-files', (_event, paths) => callback(paths)),
    onUpdateFilePath: (callback) => ipcRenderer.on('update-file-path', (_event, paths) => callback(paths)),
    onSavedFile: (callback) => ipcRenderer.on('file-saved', (_event, path) => callback(path)),
    onChangedFile: (callback) => ipcRenderer.on('file-changed', (_event, path, data) => callback(path, data)),
    onDeletedFile: (callback) => ipcRenderer.on('file-deleted', (_event, path) => callback(path)),
});