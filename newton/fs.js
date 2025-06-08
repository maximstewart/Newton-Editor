const { dialog } = require('electron');
const path = require('node:path');
const fs   = require('node:fs');
const os   = require('os')



const HOME_DIR              = os.homedir();
const BASE_PATH             = '../build/app';
const CONFIG_PATH           = path.join(HOME_DIR, "/.config/newton/");
const SETTINGS_CONFIG_PATH  = path.join(CONFIG_PATH, "/settings.json");
const LSP_CONFIG_PATH       = path.join(BASE_PATH, "/resources/lsp-servers-config.json")
let window                  = null;


const getIconPath = () => {
    return path.join(CONFIG_PATH, "./icons/newton.png");
}

const getSettingsConfigData = () => {
    return getFileContents(SETTINGS_CONFIG_PATH);
}

const getLspConfigData = () => {
    const config = getFileContents(LSP_CONFIG_PATH, useRelativePath = true);
    return config.replaceAll("{user.home}", HOME_DIR);
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
            defaultPath: (startPath) ? startPath : HOME_DIR,
            filters: [
                { name: "All Files", extensions: ["*"]                               },
                { name: "c",         extensions: [".h", ".c"]                        },
                { name: "cpp",       extensions: ["hpp", "cpp"]                      },
                { name: "html",      extensions: ["js", "css", "scss", "html", "ts"] },
                { name: "java",      extensions: ["java"]                            },
                { name: "python",    extensions: ["py", "pyc"]                       },
                { name: "rust",      extensions: ["r", "rc"]                         },
                { name: "text",      extensions: ["txt", "log", "md"]                },
                { name: "go",        extensions: ["go"]                              },
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
        getIconPath: getIconPath,
        getFileContents: getFileContents,
        getLspConfigData: getLspConfigData,
        getSettingsConfigData: getSettingsConfigData,
        setWindow: setWindow
    }
};