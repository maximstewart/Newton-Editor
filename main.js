try {
    require('electron-reloader')(module)
} catch {}



const { app, ipcMain, dialog } = require('electron');
const { newton } = require('./app');
const path = require('node:path');
const fs   = require('node:fs');



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

const saveFile = (path, content)  => {
    console.log("...");
}

const saveFileAs = (content) => {
    console.log(content);
    dialog.showSaveDialog((fileName) => {
        console.log(fileName);

        if (fileName === undefined){
            console.log("You didn't save the file");
            return;
        }

        // fileName is a string that contains the path and filename created in the save file dialog.
        fs.writeFile(fileName, content, (err) => {
            if(err){
                alert("An error ocurred creating the file "+ err.message)
            }

            alert("The file has been succesfully saved");
        });
    });
}

const loadHandlers = () => {
    ipcMain.handle('getLspConfigData', (eve) => newton.getLspConfigData());
    ipcMain.handle('getFileContents', (eve, file) => newton.getFileContents(file));
    ipcMain.handle('saveFile', (eve, path, content) => saveFile(path, "Some text to save into the file"));
    ipcMain.handle('saveFileAs', (eve, content) => saveFileAs("Some text to save into the file"));
}

app.whenReady().then(() => {
    loadArgs();
    loadHandlers();
    newton.createWindow(startType, isDebug, args);
})
 
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        newton.createWindow(startType, isDebug, args);
    };
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    };
})

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