try {
    require('electron-reloader')(module)
} catch {}


const { app, ipcMain } = require('electron');

const { newton } = require('./app');



const loadHandlers = () => {
    ipcMain.handle('getLspConfigData', (eve) => newton.fs.getLspConfigData());
    ipcMain.handle('getFileContents', (eve, file) => newton.fs.getFileContents(file));
    ipcMain.handle('openFiles', (eve, startPath) => newton.fs.openFiles(startPath));
    ipcMain.handle('saveFile', (eve, path, content) => newton.fs.saveFile(path, content));
    ipcMain.handle('saveFileAs', (eve, content) => newton.fs.saveFileAs(content));
}


app.whenReady().then(() => {
    newton.args.loadArgs();
    loadHandlers();

    newton.settings.loadsettings();
    let window = newton.createWindow(
        newton.args.getStartType(),
        newton.args.debugMode(),
        newton.args.getArgs(),
    );
    newton.fs.setWindow(window);
});
 
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        newton.createWindow(
            newton.args.getStartType(),
            newton.args.debugMode(),
            newton.args.getArgs(),
        );
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