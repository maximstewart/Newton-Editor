const { dialog } = require('electron');
const path = require('node:path');
const fs   = require('node:fs');
const os   = require('os')



const BASE_PATH       = '../dist/app';
const LSP_CONFIG_PATH = `${BASE_PATH}/resources/lsp-servers-config.json`;
let window            = null;



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

const saveFile = (fpath, content)  => {
    fs.writeFile(fpath, content, (err) => {
        if (!err) return
        console.error("An error ocurred writing to the file " + err.message)
    });
}

const saveFileAs = (content) => {
    dialog.showSaveDialog().then((response) => {
        if (response.canceled) {
            console.log("You didn't save the file");
            return;
        }

        saveFile(response.filePath, content);
    });
}

const openFiles = (startPath) => {
    dialog.showOpenDialog(
        {
            title: "Open File(s):",
            defaultPath: (startPath) ? startPath : os.homedir(),
            filters: [
                {"c": [".h", ".c"]},
                {"cpp": ["hpp", "cpp"]},
                {"html": ["js", "css", "scss", "html", "ts"]},
                {"java": ["java"]},
                {"python": ["py", "pyc"]},
                {"rust": ["r", "rc"]},
                {"text": ["txt", "log", "md"]},
                {"go": ["go"]},
            ],
            properties: [
                'openFile',
                'multiSelections'
            ]
        }
    ).then((response) => {
        if (response.canceled) {
            console.log("Canceled file open request...");
            return;
        }

        window.webContents.send('load-files', response.filePaths);
    });
}

const setWindow = (win) => {
        window = win;
}



module.exports = {
    newtonFs: {
        openFiles: openFiles,
        saveFile: saveFile,
        saveFileAs: saveFileAs,
        getFileContents: getFileContents,
        getLspConfigData: getLspConfigData,
        setWindow: setWindow
    }
};