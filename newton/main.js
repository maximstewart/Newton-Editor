const { app, ipcMain } = require('electron');

app.commandLine.appendSwitch('disable-renderer-backgrounding');
app.commandLine.appendSwitch('disable-background-timer-throttling');
app.commandLine.appendSwitch('disable-backgrounding-occluded-windows');

const { newton } = require('./app');



let window       = null;
let hasExitSaved = false;



const createWindow = () => {
    window = newton.createWindow(
        newton.args.getStartType(),
        newton.args.getDebugMode(),
        newton.args.getArgs(),
    );
}

const handleExitSignal = (code) => {
    if (!hasExitSaved) {
        newton.settings.saveConfig(window);
        hasExitSaved = true;
    }

    process.exit(code);
}


const loadProcessSignalHandlers = () => {
    process.on('SIGINT', () => {
        // https://nodejs.org/docs/v14.16.0/api/process.html#process_signal_events
        handleExitSignal(128 + 2);
    });

    process.on('SIGTERM', () => {
        // https://nodejs.org/docs/v14.16.0/api/process.html#process_signal_events
        handleExitSignal(128 + 15);
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

}

const loadHandlers = () => {
    ipcMain.handle('quit', (eve) => app.quit());
    ipcMain.handle('toggleFullScreen', (eve) => { window.setFullScreen(!window.isFullScreen()); });
    ipcMain.handle('getLspConfigData', (eve) => newton.fs.getLspConfigData());
    ipcMain.handle('getFileContents', (eve, path) => newton.fs.getFileContents(path));
    ipcMain.handle('openFiles', (eve, startPath) => newton.fs.openFiles(startPath));
    ipcMain.handle('saveFile', (eve, path, content) => newton.fs.saveFile(path, content));
    ipcMain.handle('closeFile', (eve, path) => newton.fs.closeFile(path));
    ipcMain.handle('saveFileAs', (eve, content) => newton.fs.saveFileAs(content));
}

app.whenReady().then(async () => {
    loadProcessSignalHandlers();
    newton.args.loadArgs();

    if ( !await newton.ipc.isIPCServerUp() ) {
        newton.ipc.loadIPCServer();
    } else {
        console.log("IPCServer: Is loaded... sending files to existing app.");
        newton.ipc.sendFilesToIPC(
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
});