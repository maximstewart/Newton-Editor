try {
    require('electron-reloader')(module)
} catch {}


const { app, ipcMain } = require('electron');

const { newton } = require('./app');



let startType   = "";
let isDebug     = false;
let args        = [];



const loadArgs = () => {
    console.log("\n\nStart KArgs:");
    const hasStartAs = app.commandLine.hasSwitch("start-as");
    if (hasStartAs) {
        startType = app.commandLine.getSwitchValue("start-as");
        console.log("Has start-as switch...");
        console.log(startType);
    }

    const hasDebug = app.commandLine.hasSwitch("app-debug");
    if (hasDebug) {
        isDebug = app.commandLine.getSwitchValue("app-debug");
        console.log("Has app-debug switch...");
        console.log(isDebug);
    }

    console.log("\n\nStart VArgs:");
    args = process.argv.slice(4);  // remove up to --start-as ...
    args.forEach((val, index, array) => {
        console.log(index + ': ' + val);
        console.log();
    }); 
}

const loadHandlers = () => {
    ipcMain.handle('getLspConfigData', (eve) => newton.fs.getLspConfigData());
    ipcMain.handle('getFileContents', (eve, file) => newton.fs.getFileContents(file));
    ipcMain.handle('openFiles', (eve, startPath) => newton.fs.openFiles(startPath));
    ipcMain.handle('saveFile', (eve, path, content) => newton.fs.saveFile(path, content));
    ipcMain.handle('saveFileAs', (eve, content) => newton.fs.saveFileAs(content));
}


app.whenReady().then(() => {
    loadArgs();
    loadHandlers();

    newton.settings.loadsettings();
    let window = newton.createWindow(startType, isDebug, args);
    newton.fs.setWindow(window);
});
 
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        newton.createWindow(startType, isDebug, args);
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
