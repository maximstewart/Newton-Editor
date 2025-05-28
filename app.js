const { BrowserWindow } = require('electron');
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

//    win.removeMenu()

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

const getFileContents = (_path, useRelativePath = false) => {
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