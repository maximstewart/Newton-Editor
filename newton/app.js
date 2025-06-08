const { BrowserWindow } = require('electron');
const path = require('node:path');

const { menu } = require('./menu');
const { settingsManager } = require('./settings-manager');
const { newtonFs } = require('./fs');


const BASE_PATH = '../dist/app';
const ICON_PATH = `${BASE_PATH}/resources/newton.png`;

let args = [];



// Note:  https://tinydew4.gitbooks.io/electron/content/api/browser-window.html
const createWindow = (startType = "build", debug = false, args = []) => {
    this.args = args;
    let data  = settingsManager.getConfig();

    const win = new BrowserWindow({
        title: "Newton",
        x: data["config"]["main_window_x"],
        y: data["config"]["main_window_y"],
        width:  data["config"]["main_window_width"],
        height: data["config"]["main_window_height"],
        minWidth:  data["config"]["main_window_min_width"],
        minHeight: data["config"]["main_window_min_height"],
        show: false,
        transparent: true,
        icon: settingsManager.getIconPath(),
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            enableRemoteModule: false,
            plugins: true,
            webSecurity: true,
            sandbox: true,
        }
    });

    win.once('ready-to-show', () => {
        win.show();
        win.webContents.send('load-files', args);
    });

    menu.load(win);

    // win.setAutoHideMenuBar(true)

    if (debug == true) {
        win.webContents.openDevTools();
    }

    if (startType === "build") {
        win.loadFile(
            path.join(__dirname, `${BASE_PATH}/index.html`)
        );
    }

    if (startType === "ng-serve") {
        win.loadURL('http://localhost:4200');
    }

//    const child = new BrowserWindow({parent: win, modal: true, show: false})
//    child.loadFile(
//        path.join(__dirname, `${BASE_PATH}/index.html`)
//    );
//    child.once('ready-to-show', () => {
//        child.show()
//    });

    return win;

}



module.exports = {
    newton: {
        createWindow: createWindow,
        fs: newtonFs,
        settings: settingsManager
    }
};