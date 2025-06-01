const { BrowserWindow } = require('electron');
const path = require('node:path');

const { menu } = require('./menu');
const { newtonFs } = require('./fs');


const BASE_PATH = '../dist/app';
const ICON_PATH = `${BASE_PATH}/resources/newton.png`;

let args = [];



// Note:  https://tinydew4.gitbooks.io/electron/content/api/browser-window.html
const createWindow = (startType = "build", debug = false, args = []) => {
    this.args = args;

    const win = new BrowserWindow({
        title: "Newton",
        width:  800,
        height: 600,
        minWidth:  800,
        minHeight: 600,
        show: false,
        transparent: true,
        icon: path.join(__dirname, ICON_PATH),
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
        win.show()
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
    }
};