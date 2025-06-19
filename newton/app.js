const { BrowserWindow }   = require('electron');
const path                = require('node:path');

const { menu }            = require('./menu');
const { systemTray }      = require('./system-tray');
const { argsParser }      = require('./args-parser');
const { settingsManager } = require('./settings-manager');
const { newtonFs }        = require('./fs');
const { newtonIPC }       = require('./ipc');


const BASE_PATH = '../build/app';
const ICON_PATH = `${BASE_PATH}/resources/newton.png`;

let args = [];



// Note:  https://tinydew4.gitbooks.io/electron/content/api/browser-window.html
const createWindow = (startType = "build", debug = false, args = []) => {
    this.args    = args;
    let data     = settingsManager.getConfig();

    const window = new BrowserWindow({
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
            backgroundThrottling: false,
            webSecurity: true,
            sandbox: true,
            nodeIntegration: false,
            contextIsolation: true,
            enableRemoteModule: false,
            plugins: true,
        }
    });

    window.once('close', () => {
        settingsManager.saveConfig(window);
    });

    window.once('ready-to-show', () => {
        window.show();
        window.webContents.send('load-files', args);
    });

    menu.load(window);
    systemTray.load(menu.menuStruct);

    // window.setAutoHideMenuBar(true)

    if (debug == true) {
        window.webContents.openDevTools();
    }

    if (startType === "build") {
        window.loadFile(
            path.join(__dirname, `${BASE_PATH}/index.html`)
        );
    }

    if (startType === "ng-serve") {
        window.loadURL('http://localhost:4200');
    }

//    const childWindow = new BrowserWindow({parent: window, modal: true, show: false})
//    childWindow.loadFile(
//        path.join(__dirname, `${BASE_PATH}/index.html`)
//    );
//    childWindow.once('ready-to-show', () => {
//        childWindow.show()
//    });

    return window;
}



module.exports = {
    newton: {
        createWindow: createWindow,
        args: argsParser,
        settings: settingsManager,
        fs: newtonFs,
        ipc: newtonIPC,
    }
};