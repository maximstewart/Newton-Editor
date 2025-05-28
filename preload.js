const { contextBridge, ipcRenderer, webUtils } = require('electron')


contextBridge.exposeInMainWorld('electron', {
    node: () => process.versions.node,
    chrome: () => process.versions.chrome,
    electron: () => process.versions.electron,
});

contextBridge.exposeInMainWorld('fs', {
    getLspConfigData: () => ipcRenderer.invoke("getLspConfigData"),
    getFileContents: (file) => ipcRenderer.invoke("getFileContents", file),
    getPathForFile: (file) => webUtils.getPathForFile(file)
});
