const { BrowserWindow, Menu } = require('electron');
const path = require('node:path');
const fs   = require('node:fs');
const os   = require('os')



// const BASE_PATH       = 'dist/app/browser';
const BASE_PATH       = 'dist/app';
const ICON_PATH       = `${BASE_PATH}/resources/newton.png`;
const LSP_CONFIG_PATH = `${BASE_PATH}/resources/lsp-servers-config.json`;
let args = [];



const createWindow = (startType = "build", debug = false, args = []) => {
    this.args = args;

    const win = new BrowserWindow({
        width:  800,
        height: 600,
        transparent: true,
        icon: path.join(__dirname, ICON_PATH),
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            enableRemoteModule: false,
        }
    });

    setupMenu(win);

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
}

const setupMenu = (win) => {
    const menu = Menu.buildFromTemplate([
        {
            label: "File",
            submenu: [
                {
                    label: 'New',
                    click: () => win.webContents.send('menu-actions', "new-file")
                }, {
                    label: 'Open',
                    click: () => win.webContents.send('load-files', [path.join(__dirname, `${BASE_PATH}/index.html`)])
                }, {
                    label: 'Terminal',
                    click: () => {}
                }, {
                    label: 'save',
                    click: () => win.webContents.send('menu-actions', "save-file")
                }, {
                    label: 'Save As',
                    click: () => win.webContents.send('menu-actions', "save-file-as")
                }
            ]
        }, {
            label: "Edit",
            submenu: [
                {
                    label: 'Undo',
                    click: () => win.webContents.send('menu-actions', "undo")
                }, {
                    label: 'Redo',
                    click: () => win.webContents.send('menu-actions', "redo")
                }, {
                    label: 'Cut',
                    click: () => win.webContents.send('menu-actions', "cut")
                }, {
                    label: 'Copy',
                    click: () => win.webContents.send('menu-actions', "copy")
                }, {
                    label: 'Paste',
                    click: () => win.webContents.send('menu-actions', "paste")

                }, {
                    label: 'Delete',
                    click: () => win.webContents.send('menu-actions', "delete")
                }, {
                    label: 'Select All',
                    click: () => win.webContents.send('menu-actions', "select-all")
                }, {
                    label: 'Indent',
                    click: () => win.webContents.send('menu-actions', "blockindent")
                }, {
                    label: 'De-Indent',
                    click: () => win.webContents.send('menu-actions', "blockoutdent")
                }, {
                    label: 'To Upper Case',
                    click: () => win.webContents.send('menu-actions', "touppercase")
                }, {
                    label: 'To Lower Case',
                    click: () => win.webContents.send('menu-actions', "tolowercase")
                },
            ]
        }, {
            label: "View",
            submenu: [
                {
                    label: 'Zoom In',
                    click: () => win.webContents.send('menu-actions', "zoom-in")
                }, {
                    label: 'Zoom Out',
                    click: () => win.webContents.send('menu-actions', "zoom-out")
                }, {
                    label: 'Toggle Full Screen',
                    click: () => { win.setFullScreen(!win.fullScreen) }
                }, {
                    label: 'Toggle Developer Tools',
                    click: () => win.webContents.toggleDevTools()
                }
            ]
        }, {
            label: "Help",
            submenu: [
                {
                    label: 'About',
                    click: () => win.webContents.send('menu-actions', "show-about")
                }
            ]
        },

    ]);

    Menu.setApplicationMenu(menu)
}

const getFileContents = (_path, useRelativePath = false) => {
    console.log(`Getting Contents For: ${_path}`);

    try {
        if (!useRelativePath) {
            return fs.readFileSync(_path, 'utf8');
        } else {
            return fs.readFileSync(path.join(__dirname, _path), 'utf8');
        }
    } catch(err) {
        return `{"message": {"type": "error", "text": "Error: Could not read  ${_path}"}}`;
    }
}

const getLspConfigData = () => {
    const config = getFileContents(LSP_CONFIG_PATH, true);
    return config.replaceAll("{user.home}", os.homedir());
}



module.exports = {
    newton: {
        createWindow: createWindow,
        getFileContents: getFileContents,
        getLspConfigData: getLspConfigData
    }
};