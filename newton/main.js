try {
    require('electron-reloader')(module)
} catch(error) {
    console.log(error);
}

const { app, ipcMain } = require('electron');

const { newton } = require('./app');


let window = null;


const loadHandlers = () => {
    ipcMain.handle('getLspConfigData', (eve) => newton.fs.getLspConfigData());
    ipcMain.handle('getFileContents', (eve, path) => newton.fs.getFileContents(path));
    ipcMain.handle('openFiles', (eve, startPath) => newton.fs.openFiles(startPath));
    ipcMain.handle('saveFile', (eve, path, content) => newton.fs.saveFile(path, content));
    ipcMain.handle('closeFile', (eve, path) => newton.fs.closeFile(path));
    ipcMain.handle('saveFileAs', (eve, content) => newton.fs.saveFileAs(content));
}

const createWindow = () => {
    window = newton.createWindow(
        newton.args.getStartType(),
        newton.args.debugMode(),
        newton.args.getArgs(),
    );
}


app.whenReady().then(async () => {
    newton.args.loadArgs();

    if ( !await newton.ipc.isIPCServerUp() ) {
        newton.ipc.loadIPCServer();
    } else {
        console.log("IPCServer: Is loaded... sending files to existing app.");
        await newton.ipc.sendFilesToIPC(
            newton.args.getArgs()
        );
        app.quit();
    }

    newton.settings.loadsettings();
    newton.fs.loadFilesWatcher();

    loadHandlers();
    createWindow();

    newton.fs.setWindow(window);
    newton.ipc.setWindow(window);

});
 
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    };
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    };

    newton.settings.saveConfig();
});

process.on('uncaughtException', (error) => {
    if (error.message != null) {
        console.log(error.message);
    }

    if (error.stack != null) {
        console.log(error.stack);
    }
});

process.on('unhandledRejection', function(error = {}) {
    if (error.message != null) {
        console.log(error.message);
    }

    if (error.stack != null) {
        console.log(error.stack);
    }
});
